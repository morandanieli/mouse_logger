import logging

from flask import render_template, request, url_for, send_from_directory
from flask import Flask, jsonify, g
import sqlite3
import os
from flask_cors import CORS

DIRNAME = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(DIRNAME, "db", 'user_behaviour_tracking.db')
IMAGES = os.path.join(DIRNAME, "images")


def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource(os.path.join(DIRNAME, "db", 'schema.sql'), mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


app = Flask(__name__)
CORS(app)
with app.app_context():
    init_db(app)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')


@app.route('/submit_form', methods=['POST'])
def handle_submit_request():
    try:
        content = request.json
        db = get_db()
        cur = db.cursor()
        cur.executemany(
            'INSERT INTO moves (x, y, timestamp, session_id, event_type) \
            VALUES(:x, :y, :timestamp, :session_id, :event_type);',
            content['moves']
        )
        cur.executemany(
            'INSERT INTO keys (key, keyCode, timestamp, session_id, event_type) \
            VALUES(:key, :keyCode, :timestamp, :session_id, :event_type);',
            content['keys']
        )

        db.commit()
        return {"result": "success"}

    except Exception as e:
        logging.error(e)
        return {"result": "error"}


@app.route('/clickHeatmapData', methods=['GET'])
def click_heatmap_data():
    try:
        db = get_db()
        cur = db.cursor()
        data = cur.execute(
            'select x,y,count(*) as value from moves where event_type = "click" GROUP BY x, y;'
        )
        db.commit()
        result = [{"x": item[0], "y": item[1], "value": item[2]} for item in data]
        return jsonify(result)

    except Exception as e:
        logging.error(e)
        return {}


@app.route('/status/<task_id>')
def task_status(task_id):
    task = func1.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'queue_state': task.state,
            'status': 'Process is ongoing...',
            'status_update': url_for('task_status', task_id=task.id)
        }
    else:
        response = {
            'queue_state': task.state,
            'result': task.wait()
        }
    return response


@app.route('/images/<path:path>')
def get_image(path):
    return send_from_directory('images', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')