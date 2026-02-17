from flask import Flask, redirect, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
import forms
from config import DevelopmentConfig
from models import db, Alumnos


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


@app.route("/")
@app.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    # ORM SELECT * FROM alumnos;
    alumnos = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumnos=alumnos)


@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    create_form = forms.UserForm2(request.form)
    if request.method == "POST":
        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apellido=create_form.apaterno.data,
            email=create_form.correo.data,
        )
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("alumnos.html", form=create_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()