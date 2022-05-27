from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
import psycopg2
from redis import Redis
import json

from deserialization import deserialize_holders

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

pg_conn = psycopg2.connect(database='postgres', user='postgres', password='changeme', host='localhost', port=5432,
                           cursor_factory=RealDictCursor)
pg_conn.autocommit = True

redis_conn = Redis(port=26596, password='redis', decode_responses=True)


@app.route('/holders')
def get_holders():
    try:
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        redis_key = f'holders:offset={offset},limit={limit}'
        redis_holders = redis_conn.get(redis_key)

        if redis_holders is None:
            cur = pg_conn.cursor()
            query = """
            with limited_holders as (select * from holder offset %s limit %s)
            select phone as "holderPhone", name as "holderName", "equipmentTitle", color as "equipmentColor",
                code as "storageCellCode", capacity as "storageCellCapacity"
            from limited_holders
                    left join "equipmentToHolder" on phone = "equipmentToHolder"."holderPhone"
                    left join equipment on "equipmentTitle" = title
                    left join "storageCell" on phone = "storageCell"."holderPhone";
            """

            cur.execute(query, (offset, limit))
            rows = cur.fetchall()
            cur.close()
            holders = deserialize_holders(rows)

            redis_holders = json.dumps(holders, default=vars, ensure_ascii=False, indent=2)
            redis_conn.set(redis_key, redis_holders, ex=30)

        return redis_holders, 200, {'content-type': 'text/json'}
    except Exception as ex:
        return {'message': repr(ex)}, 400


@app.route('/holders/create', methods=['POST'])
def create_holder():
    try:
        body = request.json
        name = body['name']
        phone = body['phone']

        cur = pg_conn.cursor()
        query = f"""
        insert into holder (phone, name)
        values (%s, %s)
        returning phone, name
        """

        cur.execute(query, (phone, name))
        result = cur.fetchall()
        cur.close()
        return {'message': f'Holder {result[0]["name"]} with phone = {result[0]["phone"]} created.'}
    except Exception as ex:
        return {'message': repr(ex)}, 400


@app.route('/holders/update', methods=['POST'])
def update_holder():
    try:
        body = request.json
        name = body['name']
        phone = body['phone']

        cur = pg_conn.cursor()
        query = f"""
        update holder
        set name = %s
        where phone = %s
        returning phone
        """

        cur.execute(query, (name, phone))
        affected_rows = cur.fetchall()
        cur.close()

        if len(affected_rows):
            return {'message': f'Holder with phone = {phone} updated.'}
        else:
            return {'message': f'Holder with phone = {phone} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400


@app.route('/holders/delete', methods=['DELETE'])
def delete_holder():
    try:
        body = request.json
        phone = body['phone']

        cur = pg_conn.cursor()
        query = f"""
        delete from holder
        where phone = %s
        returning phone
        """

        cur.execute(query, (phone,))
        affected_rows = cur.fetchall()
        cur.close()

        if len(affected_rows):
            return {'message': f'Holder with phone = {phone} deleted.'}
        else:
            return {'message': f'Holder with phone = {phone} not found.'}, 404
    except Exception as ex:
        return {'message': repr(ex)}, 400
