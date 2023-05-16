from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
import psycopg2
import os
import logging

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_pg_connection():
    pg_conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST') or '127.0.0.1', port=os.getenv('POSTGRES_PORT'),
                               database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'),
                               password=os.getenv('POSTGRES_PASSWORD'), cursor_factory=RealDictCursor)
    pg_conn.autocommit = True
    return pg_conn


@app.route('/holders/find_by_name', methods=['POST'])
def find_holder_by_name():
    try:
        name = request.json['name']

        query = f"""
        select *
        from holder
        where name = '{name}'
        """

        with get_pg_connection() as pg_conn, pg_conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return jsonify(rows)
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400
