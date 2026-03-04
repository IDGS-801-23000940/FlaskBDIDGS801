from . import alumnos
import forms
from flask import redirect, render_template, request, url_for
from models import Alumnos, db


@alumnos.route("/index")
def index():
    create_form = forms.UserForm(request.form)

    alumnos_lista = Alumnos.query.all()

    return render_template(
        "alumnos/index.html",
        form=create_form,
        alumnos=alumnos_lista
    )


@alumnos.route("/alumnos", methods=["GET", "POST"])
def agregar_alumno():

    create_form = forms.UserForm2(request.form)

    if request.method == "POST":

        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )

        db.session.add(alumno)
        db.session.commit()

        return redirect(url_for("alumnos.index"))

    return render_template("alumnos/alumnos.html", form=create_form)


@alumnos.route('/detalles')
def detalles():

    id = request.args.get('id')

    alumno = Alumnos.query.get(id)

    return render_template(
        "alumnos/detalles.html",
        id=alumno.id,
        nombre=alumno.nombre,
        apellidos=alumno.apellidos,
        email=alumno.email,
        telefono=alumno.telefono
    )


@alumnos.route("/modificar", methods=['GET', 'POST'])
def modificar():

    form = forms.UserForm2(request.form)

    if request.method == 'GET':

        id = request.args.get('id')

        alumno = Alumnos.query.get(id)

        if alumno:
            form.id.data = alumno.id
            form.nombre.data = alumno.nombre
            form.apellidos.data = alumno.apellidos
            form.email.data = alumno.email
            form.telefono.data = alumno.telefono

    if form.validate_on_submit():

        id = form.id.data

        alumno = Alumnos.query.get(id)

        if alumno:
            alumno.nombre = form.nombre.data
            alumno.apellidos = form.apellidos.data
            alumno.email = form.email.data
            alumno.telefono = form.telefono.data

            db.session.commit()

        return redirect(url_for("alumnos.index"))

    return render_template("alumnos/modificar.html", form=form)


@alumnos.route('/eliminar', methods=['GET', 'POST'])
def eliminar():

    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':

        id = request.args.get('id')

        alumno = Alumnos.query.get(id)

        if alumno:
            create_form.id.data = alumno.id
            create_form.nombre.data = alumno.nombre
            create_form.apellidos.data = alumno.apellidos
            create_form.email.data = alumno.email
            create_form.telefono.data = alumno.telefono

    if request.method == 'POST':

        id = create_form.id.data

        alumno = Alumnos.query.get(id)

        if alumno:
            db.session.delete(alumno)
            db.session.commit()

        return redirect(url_for("alumnos.index"))

    return render_template("alumnos/eliminar.html", form=create_form)