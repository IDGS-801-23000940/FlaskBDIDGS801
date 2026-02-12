from wtforms import Form, StringField
from wtforms import EmailField
from wtforms import validators
from wtforms import IntegerField, PasswordField, FloatField
from flask_wtf import FlaskForm

class UserForm(Form):
    matricula = IntegerField('Matricula', [validators.DataRequired(message="Campo Requerido"),
    validators.NumberRange(min=10, max=100, message="Ingrese valor valido")])
    nombre = StringField('Nombre' ,[validators.DataRequired(message="Campo Requerido"),
    validators.Length(min=2, max=20, message="Ingrese valor valido")])
    apaterno = StringField('Apellido Paterno' ,[validators.DataRequired(message="Campo Requerido")])
    amaterno = StringField('Apellido Materno' ,[validators.DataRequired(message="Campo Requerido")])
    correo = EmailField('Correo', [validators.Email(message='Ingresa un correo valido')])


class UserForm2(Form):
    id=IntegerField('id',
                    [validators.number_range(min=1, max=20, message='Valor invalido')])
    nombre = StringField('nombre',
                         [validators.DataRequired(message='El nombre es requerido'),
                          validators.length(min=4 ,max=20, message='Requiere min 4 y max 20')])
    apaterno = StringField('nombre',
                         [validators.DataRequired(message='El apellido es requerido')])
    email = EmailField('correo', [
        validators.DataRequired(message='Correo es requerido'),
        validators.Email(message='Ingrese un correo valido')
    ])