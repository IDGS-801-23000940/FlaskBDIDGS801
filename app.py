from flask import Flask, redirect, render_template, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from flask_migrate import Migrate

# IMPORTAR BLUEPRINTS
from maestros.routes import maestros
from alumnos.routes import alumnos  
from cursos import cursos              # Importamos el blueprint de cursos
from inscripciones import inscripciones # Importamos el blueprint de inscripciones

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

# Registrar blueprints
app.register_blueprint(maestros)
app.register_blueprint(alumnos)
app.register_blueprint(cursos)         # Registramos cursos
app.register_blueprint(inscripciones)  # Registramos inscripciones

db.init_app(app)

csrf = CSRFProtect()
migrate = Migrate(app, db)


# Ruta principal
@app.route("/")
def home():
     return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":

    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()