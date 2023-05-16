from flask import Flask, jsonify
import os
import logging
import clickhouse_connect


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_clickhouse_connection():
    host = os.getenv('CLICKHOUSE_HOST') or '127.0.0.1'
    port = os.getenv('CLICKHOUSE_PORT')
    user = os.getenv('CLICKHOUSE_USER')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    return clickhouse_connect.get_client(host=host, username=user, password=password, port=port, database='postgres_repl')


@app.route('/storage_cells')
def search_by_equipment():
    try:
        with get_clickhouse_connection() as ch:
            result = ch.query('select * from storage_cell')

        return jsonify(result.result_set)
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400
