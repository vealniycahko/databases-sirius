import os, logging, json, psycopg2, clickhouse_connect

from flask import Flask, request, jsonify, send_file
from psycopg2.extras import RealDictCursor, Json
from redis import Redis
from elasticsearch import Elasticsearch

from des_companies import des_companies


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def get_pg_connection():
    pg_conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST') or '127.0.0.1', 
                               port=os.getenv('POSTGRES_PORT'),
                               database=os.getenv('POSTGRES_DB'), 
                               user=os.getenv('POSTGRES_USER'),
                               password=os.getenv('POSTGRES_PASSWORD'), 
                               cursor_factory=RealDictCursor)
    pg_conn.autocommit = True
    return pg_conn

def get_pg_conn_replica():
    pg_conn = psycopg2.connect(host=os.getenv('REPLICA_HOST') or '127.0.0.1', 
                               port=os.getenv('SLAVE_PORT'),
                               database=os.getenv('POSTGRES_DB'), 
                               user=os.getenv('POSTGRES_USER'),
                               password=os.getenv('POSTGRES_PASSWORD'), 
                               cursor_factory=RealDictCursor)
    pg_conn.autocommit = True
    return pg_conn

def get_redis_connection():
    return Redis(host=os.getenv('REDIS_HOST') or '127.0.0.1', 
                 port=os.getenv('REDIS_PORT'),
                 password=os.getenv('REDIS_PASSWORD'), 
                 decode_responses=True)

def get_elastic_connection():
    host = os.getenv('ELASTIC_HOST') or '127.0.0.1'
    port = os.getenv('ELASTIC_PORT')
    return Elasticsearch(hosts=f'http://{host}:{port}')

def get_clickhouse_connection():
    host = os.getenv('CLICKHOUSE_HOST') or '127.0.0.1'
    port = os.getenv('CLICKHOUSE_PORT')
    user = os.getenv('CLICKHOUSE_USER')
    password = os.getenv('CLICKHOUSE_PASSWORD')
    return clickhouse_connect.get_client(host=host, username=user, password=password, port=port, database='postgres_repl')


@app.route('/companies', methods=['GET'])
def get_companies():
    try:
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        redis_key = f'companies:offset={offset},limit={limit}'
        with get_redis_connection() as redis_conn:
            redis_companies = redis_conn.get(redis_key)
        if redis_companies is None:
            query = """
            select co.id as c_id, co.title, co.founded, co.field, 
            wk.id as w_id, wk.f_name, wk.s_name, wk.age, wk.education
            from company as co
            left join company_worker on co.id = company_worker.company_id
            left join worker as wk on wk.id = company_worker.worker_id
            offset %s
            limit %s
            """
            with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (offset, limit))
                rows = cur.fetchall()
            companies = des_companies(rows)
            redis_companies = json.dumps(companies, default=vars, ensure_ascii=False, indent=2)
            with get_redis_connection() as redis_conn:
                redis_conn.set(redis_key, redis_companies, ex=30)
        return redis_companies, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/companies/create', methods=['POST'])
def create_company():
    try:
        body = request.json
        title = body['title']
        founded = body['founded']
        field = body['field']
        query = f"""
        insert into company (title, founded, field)
        values (%s, %s, %s)
        returning title, founded, field
        """
        with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (title, founded, field))
                result = cur.fetchall()
        return {'message': f'Company {result[0]["title"]} with founded {result[0]["founded"]} and field {result[0]["field"]} created.'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/companies/update', methods=['POST'])
def update_company():
    try:
        body = request.json
        c_id = body['id']
        title = body['title']
        query = """
        update company
        set title = %s
        where id = %s
        returning id
        """
        with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (title, c_id))
                affected_rows = cur.fetchall()
        if len(affected_rows):
            return {'message': f'Company with id = {c_id} updated.'}
        else:
            return {'message': f'Company with id = {c_id} not found.'}, 404
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/companies/delete', methods=['DELETE'])
def delete_company():
    try:
        body = request.json
        c_id = body['id']
        query = """
        delete from company
        where id = %s
        returning id
        """
        with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (c_id,))
                affected_rows = cur.fetchall()
        if len(affected_rows):
            return {'message': f'Company with id = {c_id} deleted.'}
        else:
            return {'message': f'Company with id = {c_id} not found.'}, 404
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/workers/age_histogram')
def get_age_histogram():
    try:
        redis_key = 'age_histogram'
        with get_redis_connection() as redis_conn:
            redis_age_histogram = redis_conn.get(redis_key)
        if redis_age_histogram is None:
            query = """
            with max_age as (select max(age) as age from worker),
                 histogram as (select width_bucket(age, 0, (select age from max_age), 10) as bucket,
                                      count(*)                                            as frequency
                               from worker
                               group by bucket)
            select bucket,
                   frequency,
                   (bucket - 1) * (select age / 10 from max_age) as range_from,
                   bucket * (select age / 10 from max_age)       as range_to
            from histogram
            order by bucket;
            """
            with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query)
                age_histogram = cur.fetchall()
            redis_age_histogram = json.dumps(age_histogram, default=vars, ensure_ascii=False, indent=2)
            with get_redis_connection() as redis_conn:
                redis_conn.set(redis_key, redis_age_histogram, ex=30)
        return redis_age_histogram, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/workers/index_search')
def workers_index_search():
    try:
        redis_key = 'workers_search'
        with get_redis_connection() as redis_conn:
            redis_workers_search = redis_conn.get(redis_key)
        if redis_workers_search is None:
            body = request.json
            age_from = body['age_from']
            age_to = body['age_to']
            query = """
            select *
            from worker
            where age >= %s
            and age <= %s;
            """
            with get_pg_conn_replica() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (age_from, age_to))
                workers_search = cur.fetchall()
            redis_workers_search = json.dumps(workers_search, default=vars, ensure_ascii=False, indent=2)
            with get_redis_connection() as redis_conn:
                redis_conn.set(redis_key, redis_workers_search, ex=30)
        return redis_workers_search, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/mat_view/index_search')
def mat_view_search():
    try:
        redis_key = 'mat_view_search'
        with get_redis_connection() as redis_conn:
            redis_mat_view_search = redis_conn.get(redis_key)
        if redis_mat_view_search is None:
            body = request.json
            age_from = body['age_from']
            age_to = body['age_to']
            founded_from = body['founded_from']
            founded_to = body['founded_to']
            ent_value_from = body['ent_value_from']
            ent_value_to = body['ent_value_to']
            query = """
            select *
            from company_worker_link
            where age >= %s
            and age <= %s
            and founded >= %s
            and founded <= %s
            and enterprise_value >= %s
            and enterprise_value <= %s;
            """
            with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (age_from, age_to, founded_from, founded_to, ent_value_from, ent_value_to))
                mat_view_search = cur.fetchall()
            redis_mat_view_search = json.dumps(mat_view_search, default=vars, ensure_ascii=False, indent=2)
            with get_redis_connection() as redis_conn:
                redis_conn.set(redis_key, redis_mat_view_search, ex=30)
        return redis_mat_view_search, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/workers/json_position')
def json_position_search():
    try:
        redis_key = 'json_position'
        with get_redis_connection() as redis_conn:
            redis_json_position = redis_conn.get(redis_key)
        if redis_json_position is None:
            body = request.json
            position = body['position']
            query_param = [{"position": position}]
            query = """
            select *
            from worker
            where info @> %s;
            """
            with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (Json(query_param), ))
                json_position = cur.fetchall()
            redis_json_position = json.dumps(json_position, default=vars, ensure_ascii=False, indent=2)
            with get_redis_connection() as redis_conn:
                redis_conn.set(redis_key, redis_json_position, ex=30)
        return redis_json_position, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/companies/array_search')
def companies_array_search():
    try:
        redis_key = 'array_search'
        with get_redis_connection() as redis_conn:
            redis_array_search = redis_conn.get(redis_key)
        if redis_array_search is None:
            body = request.json
            city = body['city']
            query = """
            select *
            from company
            where affiliates && array [%s];
            """
            with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
                cur.execute(query, (city, ))
                array_search = cur.fetchall()
            redis_array_search = json.dumps(array_search, default=vars, ensure_ascii=False, indent=2)
            with get_redis_connection() as redis_conn:
                redis_conn.set(redis_key, redis_array_search, ex=30)
        return redis_array_search, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/workers/match_search')
def workers_match_search():
    try:
        education = request.args.get('education')
        query = {
            "term": {
                "education": education
            }
        }
        with get_elastic_connection() as es:
            es_resp = es.search(index='worker', query=query)
        workers = []
        for hit in es_resp['hits']['hits']:
            worker = hit['_source']
            worker.pop('_meta', None)
            workers.append(worker)
        json_workers = json.dumps(workers, default=str, ensure_ascii=False, indent=2)
        return json_workers, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/workers/aggregations')
def workers_aggregations():
    try:
        query = {
            "aggs": {
                "max_age": {
                    "max": {
                        "field": "age"
                    }
                },
                "min_age": {
                    "min": {
                        "field": "age"
                    }
                },
                "avg_age": {
                    "avg": {
                        "field": "age"
                    }
                },
                "total_age": {
                    "sum": {
                        "script": "return doc['age'].value"
                    }
                }
            },
            "size": 0
        }
        with get_elastic_connection() as es:
            es_resp = es.search(index='worker', body=query)
        json_aggs = json.dumps(es_resp['aggregations'], default=str, ensure_ascii=False, indent=2)
        return json_aggs, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/companies/synonym_search')
def companies_synonym_search():
    try:
        title = request.args.get('title')
        query = {
            "match": {
                "title": {
                    "query": title,
                    "analyzer": "title_analyzer"
                }
            }
        }
        with get_elastic_connection() as es:
            es_resp = es.search(index='company', query=query)
        companies = []
        for hit in es_resp['hits']['hits']:
            company = hit['_source']
            company.pop('_meta', None)
            companies.append(company)
        json_companies = json.dumps(companies, default=str, ensure_ascii=False, indent=2)
        return json_companies, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/')
def autocomplete_page():
    try:
        return send_file('static/autocomplete.html')
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/autocomplete')
def autocomplete():
    try:
        word = request.args.get('word')
        query = {
            "match": {
                "f_name": {
                    "query": word,
                    "analyzer": "my_ngram_analyzer"
                }
            }
        }
        with get_elastic_connection() as es:
            es_resp = es.search(index='worker', query=query)
        return jsonify(list(map(lambda hit: hit['_source']['f_name'], es_resp['hits']['hits'])))
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/workers/agg_by_education')
def workers_agg_by_education():
    try:
        query = """
        select education, count(id) as count, sum(age) as total_age
        from worker
        group by education
        """
        with get_clickhouse_connection() as ch:
            result = ch.query(query)
        json_workers = json.dumps(result.result_set, default=str, ensure_ascii=False, indent=2)
        return json_workers, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/companies/founded_range')
def companies_founded_range():
    try:
        query = """
        select title, enterprise_value
        from company
        where founded >= 2000
        """
        with get_clickhouse_connection() as ch:
            result = ch.query(query)
        json_companies = json.dumps(result.result_set, default=str, ensure_ascii=False, indent=2)
        return json_companies, 200, {'content-type': 'text/json'}
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400
