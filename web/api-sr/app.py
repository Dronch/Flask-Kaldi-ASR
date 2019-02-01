from flask import Flask, jsonify, make_response, abort, request

from rq import Queue
from redis import Redis

import tasks
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

app.redis = Redis.from_url(app.config['REDIS_URL'])
app.queue = Queue(connection=app.redis)


@app.route('/asr', methods=['POST'])
def create_task():
    data = request.get_data()

    if not data:
        abort(400)

    job = app.queue.enqueue(tasks.wav_to_text, args=(data, app.config['TMP_DIR']))

    if not job:
        abort(500)

    return jsonify(guid=job.get_id()), 201


@app.route('/asr', methods=['GET'])
def get_tasks():
    return jsonify(app.queue.get_job_ids()), 200


@app.route('/asr/<guid>', methods=['GET'])
def get_task(guid):

    job = app.queue.fetch_job(guid)

    if not job:
        return abort(404)

    job.refresh()

    if job.is_failed:
        abort(500)

    if job.is_finished:
        result, status_code = job.result

        if status_code != 200:
            abort(status_code)

        return jsonify(result), status_code

    return jsonify(ready=False), 202


@app.errorhandler(404)
def not_found():
    return make_response(jsonify(error='Not found'), 404)


@app.errorhandler(500)
def bad_request():
    return make_response(jsonify(error='Internal error'), 500)


@app.errorhandler(400)
def bad_request():
    return make_response(jsonify(error='Bad request'), 400)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
