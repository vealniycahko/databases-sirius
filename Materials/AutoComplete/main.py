from flask import Flask, jsonify, request, send_file
from elasticsearch import Elasticsearch
import os
import logging

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_elastic_connection():
    host = os.getenv('ELASTIC_HOST') or '127.0.0.1'
    port = os.getenv('ELASTIC_PORT')

    return Elasticsearch(hosts=f'http://{host}:{port}')


@app.route('/')
def autocomplete_page():
    try:
        return send_file('static/autocomplete.html')
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400


@app.route('/holders/search_by_equipment')
def search_by_equipment():
    try:
        title = request.args.get('title')

        query = {
            "term": {
                "equipment.title": title
            }
        }

        with get_elastic_connection() as es:
            es_resp = es.search(index='holder', query=query)

        holders = []
        for hit in es_resp['hits']['hits']:
            holder = hit['_source']
            holder.pop('_meta', None)
            
            holders.append(holder)

        return jsonify(holders)
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400

@app.route('/autocomplete')
def autocomplete():
    try:
        word = request.args.get('word')

        query = {
            "match": {
                "title": {
                    "query": word,
                    "analyzer": "my_ngram_analyzer"
                }
            }
        }

        with get_elastic_connection() as es:
            es_resp = es.search(index='equipment', query=query)

        return jsonify(list(map(lambda hit: hit['_source']['title'], es_resp['hits']['hits'])))
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400
