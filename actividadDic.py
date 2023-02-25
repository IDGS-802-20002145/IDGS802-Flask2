from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, validators
from wtforms import validators

# Define la clase del formulario para la sección de guardar
class GuardarForm(Form):
    espanol = StringField('Español', [
        validators.DataRequired(message='Es necesario ingresar una palabra en español'),
        validators.InputRequired()])
    ingles = StringField('Inglés', [ 
        validators.DataRequired(message='Es necesario ingresar una palabra en ingles'),
         validators.InputRequired()])

# Define la clase del formulario para la sección de búsqueda
class BuscarForm(Form):
    palabra_buscar = StringField('Palabra', [ 
        validators.DataRequired(message='Es necesario ingresar una palabra para realizar la busqueda'),
        validators.InputRequired()])
    respuesta = RadioField('Idioma de búsqueda', choices=[('es', 'Español'), ('en', 'Inglés')],
        validators=[validators.InputRequired(message='Seleccione una opción')])