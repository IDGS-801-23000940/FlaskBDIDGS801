from . import inscripciones
import forms
from flask import redirect, render_template, request, url_for
from models import Alumnos, Curso, db

@inscripciones.route('/inscripciones', methods=['GET'])
def listado_inscripciones():
    # Consultamos todos los cursos para ver qué alumnos tienen inscritos
    cursos_lista = Curso.query.all()
    return render_template("inscripciones/listadoInscripciones.html", cursos=cursos_lista)

@inscripciones.route('/agregarInscripcion', methods=['GET', 'POST'])
def agregar():
    form = forms.InscripcionForm(request.form)
    
    # 1. Consultamos las listas para llenar los menús desplegables
    alumnos_lista = Alumnos.query.all()
    cursos_lista = Curso.query.all()
    
    if request.method == 'POST' and form.validate():
        alumno_id = form.alumno_id.data
        curso_id = form.curso_id.data

        # Obtenemos los objetos existentes
        alumno = Alumnos.query.get(alumno_id)
        curso = Curso.query.get(curso_id)

        if alumno and curso:
            # Validamos que el alumno no esté ya en la lista
            if alumno not in curso.alumnos:
                curso.alumnos.append(alumno) # Insertamos usando append [cite: 98, 100, 106]
                db.session.commit()
                return redirect(url_for('inscripciones.listado_inscripciones'))
            else:
                pass # Aquí podrías agregar un mensaje flash indicando que ya está inscrito
                
    # 2. Pasamos alumnos_lista y cursos_lista al render_template
    return render_template(
        "inscripciones/agregarInscripcion.html", 
        form=form, 
        alumnos=alumnos_lista, 
        cursos=cursos_lista
    )


@inscripciones.route('/detallesInscripcion', methods=['GET'])
def detalles():
    id_curso = request.args.get('id')
    # Consultamos el curso por su ID. La relación 'alumnos' de SQLAlchemy se encargará del resto.
    curso_detalle = Curso.query.get(id_curso)
    
    if not curso_detalle:
        return redirect(url_for('inscripciones.listado_inscripciones'))
        
    return render_template("inscripciones/detallesInscripcion.html", curso=curso_detalle)