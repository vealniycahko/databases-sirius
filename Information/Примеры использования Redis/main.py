from flask import Flask, jsonify, request
from redis import Redis

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

redis_conn = Redis(port=26596, password='redis', decode_responses=True)


@app.route('/')
def get_home_page():
    try:
        redis_conn.incr('visits')
        visits = redis_conn.get('visits')
        return f"""
        <h1>Hello, Redis!</h1>
        <h2>This page has been visited {visits} times!</h2>
        """
    except Exception as ex:
        return {'message': repr(ex)}, 400


@app.route('/user_actions/add', methods=['POST'])
def add_user_action():
    try:
        body = request.json
        user_name = body['user_name']
        action_name = body['action_name']
        redis_conn.lpush(f'users_actions:{user_name}', action_name)
        return {'message': f'action {action_name} for user {user_name} is added'}
    except Exception as ex:
        return {'message': repr(ex)}, 400


@app.route('/user_actions/cancel', methods=['DELETE'])
def cancel_user_action():
    try:
        body = request.json
        user_name = body['user_name']
        last_action = redis_conn.lpop(f'users_actions:{user_name}')
        return {'message': f'last action {last_action} for user {user_name} is canceled'}
    except Exception as ex:
        return {'message': repr(ex)}, 400


@app.route('/users_actions')
def get_user_actions():
    try:
        user_name = request.args.get('user_name')
        all_actions = redis_conn.lrange(f'users_actions:{user_name}', 0, -1)
        return jsonify(all_actions)
    except Exception as ex:
        return {'message': repr(ex)}, 400
