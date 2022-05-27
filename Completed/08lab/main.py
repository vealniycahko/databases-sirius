from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from redis import Redis


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

pg_conn = psycopg2.connect(database='postgres', user='postgres', password='changeme',
                           host='localhost', port=999,
                           cursor_factory=RealDictCursor)
pg_conn.autocommit = True

redis_conn = Redis(port=26596, password='redis', decode_responses=True)

import other


# ---COMPANIES-------------------------------------------------------------------------

@app.route('/companies')
def get_companies():
    try:
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        redis_key = f'companies:offset={offset},limit={limit}'
        redis_companies = redis_conn.get(redis_key)
        if redis_companies is None:
            cur = pg_conn.cursor()
            query = """
            select co.id as c_id, co.title, co.founded, co.field, 
            wk.id as w_id, wk.f_name, wk.s_name, wk.age, wk.education
            from company as co
            left join company_worker on co.id = company_worker.company_id
            left join worker as wk on wk.id = company_worker.worker_id
            offset %s
            limit %s
            """
            cur.execute(query, (offset, limit))
            rows = cur.fetchall()
            companies = des_companies(rows)
            cur.close()
            redis_companies = json.dumps(companies, default=vars, ensure_ascii=False, indent=2)
            redis_conn.set(redis_key, redis_companies, ex=30)
        return redis_companies, 200, {'content-type': 'text/json'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request GET 'http://127.0.0.1:5000/companies?offset=0&limit=100'

@app.route('/companies/create', methods=['POST'])
def create_company():
    try:
        body = request.json
        title = body['title']
        founded = body['founded']
        field = body['field']
        cur = pg_conn.cursor()
        query = f"""
        insert into company (title, founded, field)
        values (%s, %s, %s)
        returning title, founded, field
        """
        cur.execute(query, (title, founded, field))
        result = cur.fetchall()
        cur.close()
        return {'message': f'Company {result[0]["title"]} with founded {result[0]["founded"]} and field {result[0]["field"]} created.'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request POST 'http://127.0.0.1:5000/companies/create' --header 'Content-Type: application/json' --data-raw '{"title": "Ol-la", "founded": "May, 2021", "field": "Fastfood"}'

@app.route('/companies/update', methods=['POST'])
def update_company():
    try:
        body = request.json
        c_id = body['id']
        title = body['title']
        cur = pg_conn.cursor()
        query = f"""
        update company
        set title = %s
        where id = %s
        returning id
        """
        cur.execute(query, (title, c_id))
        affected_rows = cur.fetchall()
        cur.close()
        if len(affected_rows):
            return {'message': f'Company with id = {c_id} updated.'}
        else:
            return {'message': f'Company with id = {c_id} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request POST 'http://127.0.0.1:5000/companies/update' --header 'Content-Type: application/json' --data-raw '{"id": 3, "title": "Wheels and Motors"}'

@app.route('/companies/delete', methods=['DELETE'])
def delete_company():
    try:
        body = request.json
        c_id = body['id']
        cur = pg_conn.cursor()
        query = f"""
        delete from company
        where id = %s
        returning id
        """
        cur.execute(query, (c_id,))
        affected_rows = cur.fetchall()
        cur.close()
        if len(affected_rows):
            return {'message': f'Company with id = {c_id} deleted.'}
        else:
            return {'message': f'Company with id = {c_id} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request DELETE 'http://127.0.0.1:5000/companies/delete' --header 'Content-Type: application/json' --data-raw '{"id": 6}'

def des_companies(rows):
    class Company:
        def __init__(self, identify: int, title: str, founded: str, field: str):
            self.identify = identify
            self.title = title
            self.founded = founded
            self.field = field
            self.workers: list[Worker] = []

    class Worker:
        def __init__(self, identify: int, f_name: str, s_name: str, age: int, education: str):
            self.identify = identify
            self.f_name = f_name
            self.s_name = s_name
            self.age = age
            self.education = education

    companies_dict = {}
    workers_dict = {}

    for row in rows:
        c_id = row['c_id']
        title = row['title']
        founded = row['founded']
        field = row['field']

        company = None
        if c_id in companies_dict:
            company = companies_dict[c_id]
        else:
            company = Company(c_id, title, founded, field)
            companies_dict[c_id] = company

        w_id = row['w_id']
        f_name = row['f_name']
        s_name = row['s_name']
        age = row['age']
        education = row['education']

        worker = None
        if w_id in workers_dict:
            worker = workers_dict[w_id]
        else:
            worker = Worker(w_id, f_name, s_name, age, education)
            workers_dict[w_id] = worker

        if w_id is not None:
            if worker not in company.workers: 
                company.workers.append(worker)

    return list(companies_dict.values())


# ---WORKERS-------------------------------------------------------------------------

@app.route('/workers/age_histogram')
def get_age_histogram():
    try:
        redis_key = 'age_histogram'
        redis_age_histogram = redis_conn.get(redis_key)
        if redis_age_histogram is None:
            cur = pg_conn.cursor()
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
            cur.execute(query)
            age_histogram = cur.fetchall()
            cur.close()
            redis_age_histogram = json.dumps(age_histogram, default=vars, ensure_ascii=False, indent=2)
            redis_conn.set(redis_key, redis_age_histogram, ex=30)
        return redis_age_histogram, 200, {'content-type': 'text/json'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request GET 'http://127.0.0.1:5000/workers/age_histogram'
