from . import cursos
import forms
from flask import redirect, render_template, request, url_for
from models import Curso, Maestros, db

@cursos.route('/cursos', methods=['GET', 'POST'])
def listado_cursos():
    create_form = forms.CursoForm(request.form)
    # Hacemos un join con Maestros para poder mostrar el nombre del maestro en la vista si lo deseamos
    cursos_lista = Curso.query.all()
    return render_template("cursos/listadoCursos.html", form=create_form, cursos=cursos_lista)

@cursos.route('/agregarCurso', methods=['GET', 'POST'])
def agregar():
    create_form = forms.CursoForm(request.form)
    
    # 1. Consultamos TODOS los maestros para mandarlos al menú desplegable
    maestros_lista = Maestros.query.all()

    if request.method == 'POST' and create_form.validate():
        nombre = create_form.nombre.data
        descripcion = create_form.descripcion.data
        # Como el select se llama "maestro_id", WTForms lo captura aquí
        maestro_id = create_form.maestro_id.data 

        maestro_existe = Maestros.query.get(maestro_id)
        if maestro_existe:
            nuevo_curso = Curso(nombre=nombre, descripcion=descripcion, maestro_id=maestro_id)
            db.session.add(nuevo_curso)
            db.session.commit()
            return redirect(url_for('cursos.listado_cursos'))
    
    # 2. Pasamos 'maestros_lista' a la plantilla
    return render_template("cursos/agregarCurso.html", form=create_form, maestros=maestros_lista)

@cursos.route('/detallesCurso', methods=['GET'])
def detalles():
    id_curso = request.args.get('id')
    curso = db.session.query(Curso).filter(Curso.id == id_curso).first()
    
    return render_template('cursos/detallesCurso.html', curso=curso)

@cursos.route("/modificarCurso", methods=['GET', 'POST'])
def modificarCurso():
    form = forms.CursoForm(request.form)
    
    # Consultamos TODOS los maestros para poder llenar el menú desplegable (select)
    maestros_lista = Maestros.query.all()

    if request.method == 'GET':
        id_curso = request.args.get('id')
        curso = Curso.query.get(id_curso)

        if curso:
            form.id.data = curso.id
            form.nombre.data = curso.nombre
            form.descripcion.data = curso.descripcion
            form.maestro_id.data = curso.maestro_id

    # AQUÍ ESTÁ LA SOLUCIÓN: Usamos request.method == 'POST' y form.validate()
    if request.method == 'POST' and form.validate():
        id_curso = request.form.get('id') # Obtenemos el ID oculto
        curso = Curso.query.get(id_curso)

        if curso:
            curso.nombre = form.nombre.data.strip()
            curso.descripcion = form.descripcion.data
            # Actualizamos el maestro asignado
            curso.maestro_id = form.maestro_id.data
            db.session.commit()

        return redirect(url_for('cursos.listado_cursos'))
        
    # Le pasamos la variable maestros a la plantilla
    return render_template('cursos/modificarCurso.html', form=form, maestros=maestros_lista)

@cursos.route('/eliminarCurso', methods=['GET', 'POST'])
def eliminar(): 
    form = forms.CursoForm(request.form)
    if request.method == 'GET':
        id_curso = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id_curso).first()

        if curso:
            form.id.data = curso.id
            form.nombre.data = curso.nombre
            form.descripcion.data = curso.descripcion
            form.maestro_id.data = curso.maestro_id
            return render_template('cursos/eliminarCurso.html', form=form, curso=curso)
    
    if request.method == 'POST':
        id_curso = request.form.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id_curso).first()
        if curso:
            db.session.delete(curso) 
            db.session.commit()
        return redirect(url_for('cursos.listado_cursos'))
        
    return render_template('cursos/eliminarCurso.html', form=form)