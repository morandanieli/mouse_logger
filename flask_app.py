from flask import render_template, request, url_for, send_from_directory
from flask import Flask
import sqlite3
from flask import g
import os
from celery_app import func1

DIRNAME = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(DIRNAME, "db", 'logger.db')
IMAGES = os.path.join(DIRNAME, "images")

def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource(os.path.join(DIRNAME, "db", 'schema.sql'), mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def create_app():
    app = Flask(__name__,
                static_url_path='/static',
                static_folder='web/static',
                template_folder='web/templates')
    with app.app_context():
        init_db(app)
    return app


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


app = create_app()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello():
    return render_template('index.html')


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
        cur.close()

        session_id = content['moves'][0]["session_id"]
        output_filename = os.path.join(IMAGES, "{}.png".format(session_id))
        task = func1.delay(session_id, output_filename, DATABASE)
        return {"result": "success", "redirect_url": url_for('task_status', task_id=task.id)}

    except Exception as e:
        return {"result": "error"}


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
    app.run(port=5001,debug=True, host='0.0.0.0')