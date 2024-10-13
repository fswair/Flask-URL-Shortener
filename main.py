from flask import Flask, render_template
from flask_cors import CORS 
from router import url_shortener
from database import init_db

app = Flask(__name__)
CORS(app)
app.register_blueprint(url_shortener)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
