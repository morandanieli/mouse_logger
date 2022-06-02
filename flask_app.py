from flask import render_template, request
from flask import Flask
import sqlite3
from flask import g
import os

DATABASE = os.path.join("db", 'logger.db')


def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource(os.path.join("db", 'schema.sql'), mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def create_app():
    app = Flask(__name__)
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
        return {"result": "success"}
    except Exception:
        return {"result": "error"}


if __name__ == '__main__':
    app.run(port=5001,debug=True)