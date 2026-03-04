from . import maestros
import forms
from flask import redirect, render_template, request, url_for
from models import Maestros, Alumnos, db


@maestros.route('/maestros', methods=['GET','POST'])
def listado_maestros():
    create_form=forms.TeacherForm(request.form)
    maestros_lista= Maestros.query.all()
    return render_template("maestros/listadoMaestros.html", form=create_form,
                           maestros = maestros_lista)

@maestros.route('/agregarMaestros', methods=['GET','POST'])
def agregar():
    create_form = forms.TeacherForm(request.form)
    if request.method == 'POST' and create_form.validate():
        matricula = create_form.matricula.data
        nombre = create_form.nombre.data
        apellidos = create_form.apellidos.data
        especialidad = create_form.especialidad.data
        email = create_form.email.data

        nuevo_maestro = Maestros(matricula=matricula, nombre=nombre, apellidos=apellidos, especialidad=especialidad, email=email)
        db.session.add(nuevo_maestro)
        db.session.commit()
        return redirect(url_for('maestros.listado_maestros'))
    
    return render_template("maestros/agregarMaestro.html", form=create_form)


@maestros.route('/detallesMaestros', methods=['GET', 'POST'])
def detalles():
    create_form = forms.TeacherForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        #select * from maestros where matricula == matricula
        maes = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
        nombre = maes.nombre
        apellidos = maes.apellidos
        especialidad = maes.especialidad
        email = maes.email
        
    return render_template('maestros/detallesMaestros.html', matricula=matricula, nombre=nombre, apellidos=apellidos,especialidad=especialidad,  email=email)

@maestros.route("/modificarMaestros", methods= ['GET', 'POST'])
def modificarMaestro():
    form = forms.TeacherForm(request.form)
    #GET == cargar datos
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro = Maestros.query.get(matricula)

        if maestro:
            form.matricula.data = maestro.matricula
            form.nombre.data = maestro.nombre
            form.apellidos.data = maestro.apellidos
            form.especialidad.data = maestro.especialidad
            form.email.data = maestro.email
    # POST == actualizar
    if form.validate_on_submit():
        matricula = form.matricula.data
        maestro = Maestros.query.get(matricula)

        if maestro:
            maestro.nombre = form.nombre.data.strip()
            maestro.apellidos = form.apellidos.data
            maestro.especialidad = form.especialidad.data
            maestro.email = form.email.data
            db.session.commit()

        return redirect(url_for('maestros.listado_maestros'))
    return render_template('maestros/modificarMaestro.html', form=form)

@maestros.route('/eliminarMaestro', methods=['GET', 'POST'])
def eliminar(): 
    create_form = forms.TeacherForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()

        if maes:
            create_form.matricula.data = maes.matricula
            create_form.nombre.data = maes.nombre
            create_form.apellidos.data = maes.apellidos
            create_form.especialidad.data = maes.especialidad
            create_form.email.data = maes.email
            return render_template('maestros/eliminarMaestro.html', form=create_form)
    
    if request.method == 'POST':
        matricula = create_form.matricula.data
        maes = db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
        if maes:
            db.session.delete(maes) 
            db.session.commit()
        return redirect(url_for('maestros.listado_maestros'))
    return render_template('maestros/eliminarMaestro.html', form=create_form)   


@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f" Perfil de {nombre}"