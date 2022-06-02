from flask import render_template, request, jsonify
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def handle_submit_request():
    content = request.json
    print(content)
    return {"result": "success"}


if __name__ == '__main__':
    app.run(port=5000,debug=True)