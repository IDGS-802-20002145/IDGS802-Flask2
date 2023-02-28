from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField,\
SelectField, RadioField, PasswordField
from wtforms.fields import EmailField,TextAreaField
from wtforms import validators

def mi_validacion(form,field):
    if len(field.data)==0:
        raise validators.ValidationError('El campo no tiene datos')

class UserForm(Form):

    matricula=StringField('Matricula',[
        validators.DataRequired(message='La Matricula es requerida')])
    nombre=StringField('Nombre',[
        validators.DataRequired(message='Este campo no puede quedarse vacio'),
        validators.length(min=5,max=15, message='Ingresa un valor maximo')
        ])
    apaterno=StringField('Apaterno', [mi_validacion])
    amaterno=StringField('Amaterno')
    email=EmailField('Correo')

class LoginForm(Form):
     username=StringField('Usuario',[
        validators.DataRequired(message='El nombre de usuario es requerido')])
     password=PasswordField('Contraseña',[
        validators.DataRequired(message='Este campo no puede quedarse vacio'),
        validators.length(min=5,max=15, message='Ingresa un de minimo 5 caracteres o maximo 15')
        ])
     

class ResistorForm(Form):
    colors = [('', 'Seleccione una Opción'),('0', 'Negro'), ('1', 'Marrón'), ('2', 'Rojo'), ('3', 'Naranja'), ('4', 'Amarillo'), 
              ('5', 'Verde'), ('6', 'Azul'), ('7', 'Violeta'), ('8', 'Gris'), ('9', 'Blanco')]
    band1 = SelectField('1ª franja', choices=colors, validators=[validators.InputRequired('Elija una opción correcta')])
    band2 = SelectField('2ª franja', choices=colors, validators=[validators.InputRequired('Elija una opción correcta')])
    multiplier = SelectField('Multiplicador', choices=[('0', 'Negro x1 Ω'), ('1', 'Marron x10 Ω'), 
                                              ('2', 'Rojo x100 Ω'), ('3', 'Naranja x1 kΩ'),
                                              ('4', 'Amarillo x10 kΩ'), ('5', 'Verde x100 kΩ'), 
                                              ('6', 'Azul x1 MΩ'), ('7', 'Violeta x10 MΩ'),
                                              ('8', 'Gris x100 MΩ'), ('9', 'Blanco x10 GΩ'),
                                              ('10', 'Oro x0.1 Ω'), ('11', 'Plata x0.01 Ω')],
                                                       validators=[validators.InputRequired()])
    tolerance = RadioField('Tolerancia', choices=[('oro', 'ORO ± 5%'), ('plata', 'PLATA ± 10%')], 
                           validators=[validators.InputRequired(message='Este campo no puede quedarse vacio')])