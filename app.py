from flask import Flask, render_template
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g

from config import DevelopmentConfig
from models import db, Alumnos


app = Flask(__name__)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/alumnos')
def alumnos():
    return render_template('alumnos.html')

if __name__ == '__main__':
    app.run(debug=True)