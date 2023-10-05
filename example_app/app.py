from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/nutrition.html')
def questionnaire():
    return render_template('nutrition.html')


if __name__ == '__main__':
    app.run(debug=True)