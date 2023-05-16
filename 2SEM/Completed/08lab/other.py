from main import app, redis_conn, pg_conn
from flask import request, jsonify
import json


# ---WORKERS-------------------------------------------------------------------------

@app.route('/workers')
def get_workers():
    try:
        redis_key = 'workers'
        redis_workers = redis_conn.get(redis_key)
        if redis_workers is None:
            cur = pg_conn.cursor()
            query = """
            select worker.id, worker.f_name, worker.s_name, worker.age, worker.education, 
            company.id, company.title, document.id, document.type
            from worker
            left join company_worker on worker.id = company_worker.worker_id 
            left join company on company_worker.company_id = company.id 
            left join document on worker.id = document.worker
            """
            cur.execute(query)
            workers = cur.fetchall()
            cur.close()
            redis_workers = json.dumps(workers, default=vars, ensure_ascii=False, indent=2)
            redis_conn.set(redis_key, redis_workers, ex=30)
        return redis_workers, 200, {'content-type': 'text/json'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request GET 'http://127.0.0.1:5000/workers'

@app.route('/workers/create', methods=['POST'])
def create_worker():
    try:
        body = request.json
        f_name = body['f_name']
        s_name = body['s_name']
        age = body['age']
        education = body['education']
        cur = pg_conn.cursor()
        query = f"""
        insert into worker (f_name, s_name, age, education)
        values (%s, %s, %s, %s)
        returning f_name, s_name, age, education
        """
        cur.execute(query, (f_name, s_name, age, education))
        result = cur.fetchall()
        cur.close()
        return {'message': f'Worker {result[0]["f_name"]} {result[0]["s_name"]}, age - {result[0]["age"]} and education {result[0]["education"]} created.'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request POST 'http://127.0.0.1:5000/workers/create' --header 'Content-Type: application/json' --data-raw '{"f_name": "Genry", "s_name": "McAllister", "age": 45, "education": "College"}'

@app.route('/workers/update', methods=['POST'])
def update_worker():
    try:
        body = request.json
        w_id = body['id']
        education = body['education']
        cur = pg_conn.cursor()
        query = f"""
        update worker
        set education = %s
        where id = %s
        returning id
        """
        cur.execute(query, (education, w_id))
        affected_rows = cur.fetchall()
        cur.close()
        if len(affected_rows):
            return {'message': f'Worker with id = {w_id} updated.'}
        else:
            return {'message': f'Worker with id = {w_id} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request POST 'http://127.0.0.1:5000/workers/update' --header 'Content-Type: application/json' --data-raw '{"id": 3, "education": "Yale University, Bachelors degree"}'

@app.route('/workers/delete', methods=['DELETE'])
def delete_worker():
    try:
        body = request.json
        w_id = body['id']
        cur = pg_conn.cursor()
        query = f"""
        delete from worker
        where id = %s
        returning id
        """
        cur.execute(query, (w_id,))
        affected_rows = cur.fetchall()
        cur.close()
        if len(affected_rows):
            return {'message': f'Worker with id = {w_id} deleted.'}
        else:
            return {'message': f'Worker with id = {w_id} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request DELETE 'http://127.0.0.1:5000/workers/delete' --header 'Content-Type: application/json' --data-raw '{"id": 11}'


# ---DOCUMENTS-------------------------------------------------------------------------

@app.route('/documents')
def get_documents():
    try:
        redis_key = 'documents'
        redis_documents = redis_conn.get(redis_key)
        if redis_documents is None:
            cur = pg_conn.cursor()
            query = """
            select document.id, document.type, document.information, document.worker, worker.f_name, worker.s_name 
            from document
            left join worker on document.worker = worker.id
            """
            cur.execute(query)
            documents = cur.fetchall()
            cur.close()
            redis_documents = json.dumps(documents, default=vars, ensure_ascii=False, indent=2)
            redis_conn.set(redis_key, redis_documents, ex=30)
        return redis_documents, 200, {'content-type': 'text/json'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request GET 'http://127.0.0.1:5000/documents'

@app.route('/documents/create', methods=['POST'])
def create_document():
    try:
        body = request.json
        d_type = body['type']
        information = body['information']
        worker = body['worker']
        cur = pg_conn.cursor()
        query = f"""
        insert into document (type, information, worker)
        values (%s, %s, %s)
        returning type, information, worker
        """
        cur.execute(query, (d_type, information, worker))
        result = cur.fetchall()
        cur.close()
        return {'message': f'Document {result[0]["type"]} with information: {result[0]["information"]}, for worker {result[0]["worker"]} created.'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request POST 'http://127.0.0.1:5000/documents/create' --header 'Content-Type: application/json' --data-raw '{"type": "Certificate", "information": "Graduated from the leadership course", "worker": 2}'

@app.route('/documents/update', methods=['POST'])
def update_document():
    try:
        body = request.json
        d_id = body['id']
        information = body['information']
        cur = pg_conn.cursor()
        query = f"""
        update document
        set information = %s
        where id = %s
        returning id
        """
        cur.execute(query, (information, d_id))
        affected_rows = cur.fetchall()
        cur.close()
        if len(affected_rows):
            return {'message': f'Document with id = {d_id} updated.'}
        else:
            return {'message': f'Document with id = {d_id} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request POST 'http://127.0.0.1:5000/documents/update' --header 'Content-Type: application/json' --data-raw '{"id": 2, "information": "60 hours"}'

@app.route('/documents/delete', methods=['DELETE'])
def delete_document():
    try:
        body = request.json
        d_id = body['id']
        cur = pg_conn.cursor()
        query = f"""
        delete from document
        where id = %s
        returning id
        """
        cur.execute(query, (d_id,))
        affected_rows = cur.fetchall()
        cur.close()
        if len(affected_rows):
            return {'message': f'Document with id = {d_id} deleted.'}
        else:
            return {'message': f'Document with id = {d_id} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request DELETE 'http://127.0.0.1:5000/documents/delete' --header 'Content-Type: application/json' --data-raw '{"id": 4}'


# ---COMPANY-WORKER-------------------------------------------------------------------------

@app.route('/company_worker')
def get_company_worker():
    try:
        redis_key = 'company_worker'
        redis_company_worker = redis_conn.get(redis_key)
        if redis_company_worker is None:
            cur = pg_conn.cursor()
            query = """
            select company_worker.company_id, company.title, company_worker.worker_id, worker.f_name, worker.s_name 
            from company_worker
            left join company on company_worker.company_id = company.id
            left join worker on company_worker.worker_id = worker.id
            """
            cur.execute(query)
            company_worker = cur.fetchall()
            cur.close()
            redis_company_worker = json.dumps(company_worker, default=vars, ensure_ascii=False, indent=2)
            redis_conn.set(redis_key, redis_company_worker, ex=30)
        return redis_company_worker, 200, {'content-type': 'text/json'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# # curl --location --request GET 'http://127.0.0.1:5000/company_worker'

@app.route('/company_worker/create', methods=['POST'])
def create_company_worker():
    try:
        body = request.json
        company_id = body['company_id']
        worker_id = body['worker_id']
        cur = pg_conn.cursor()
        query = f"""
        insert into company_worker (company_id, worker_id)
        values (%s, %s)
        returning company_id, worker_id
        """
        cur.execute(query, (company_id, worker_id))
        result = cur.fetchall()
        cur.close()
        return {'message': f'Company_worker relation {result[0]["company_id"]} -- {result[0]["worker_id"]} created.'}
    except Exception as ex:
        return {'message': repr(ex)}, 400
# После создания нового работника и новой компании:
# curl --location --request POST 'http://127.0.0.1:5000/company_worker/create' --header 'Content-Type: application/json' --data-raw '{"company_id": 6, "worker_id": 11}'

# update здесь не нужен

@app.route('/company_worker/delete', methods=['DELETE'])
def delete_company_worker():
    try:
        body = request.json
        company_id = body['company_id']
        worker_id = body['worker_id']        
        cur = pg_conn.cursor()
        query = f"""
        delete from company_worker
        where company_id = %s and worker_id = %s
        returning company_id, worker_id
        """
        cur.execute(query, (company_id, worker_id))
        affected_rows = cur.fetchall()
        cur.close()
        if len(affected_rows):
            return {'message': f'Company_worker relation with company_id = {company_id} and worker_id = {worker_id} deleted.'}
        else:
            return {'message': f'Company_worker relation with company_id = {company_id} and worker_id = {worker_id} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
# curl --location --request DELETE 'http://127.0.0.1:5000/company_worker/delete' --header 'Content-Type: application/json' --data-raw '{"company_id": 6, "worker_id": 11}'
