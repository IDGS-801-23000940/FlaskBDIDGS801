from flask import Flask, redirect, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
import forms
from config import DevelopmentConfig
from models import db, Alumnos


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
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
            apaterno=create_form.apaterno.data,
            email=create_form.email.data,
        )
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("alumnos.html", form=create_form)

@app.route('/detalles', methods=['GET', 'POST'])
def detalles():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        #select * from alumnos where id == id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        nombre = alum1.nombre
        apaterno = alum1.apaterno
        email = alum1.email
        
    return render_template('detalles.html', id=id, nombre=nombre, apaterno=apaterno, email=email)


@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        #SELECT * FROM alumnos where id == id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data = str.rstrip(alum1.nombre)
        create_form.apaterno.data = alum1.apaterno
        create_form.email.data = alum1.email
    if request.method=='POST':
        id=create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum1.id=id
        alum1.nombre=str.rstrip(create_form.nombre.data)
        alum1.apaterno=create_form.apaterno.data
        alum1.email = create_form.email.data
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('modificar.html', form = create_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    csrf.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()