from flask import Flask, render_template
from flask import request
from collections import Counter
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask import make_response #Este es para el manejo de Cookies
from flask import flash #Esta es para ensajes flash, son avisos que van en la vista para el usuario 



import forms
import actividad1
import actividadDic

app=Flask(__name__)



app.config['SECRET_KEY'] = "Esta es una clave encriptada"
app.config.from_object(Config)
csrf= CSRFProtect()


@app.errorhandler(404)
def no_encontrada(e):
    return render_template('404.html'),404

@app.before_request
def before_request():
    print('numero1')

@app.route("/cookies", methods=['GET','POST'])
def cookies():
    print('numero2')

    reg_user=forms.LoginForm(request.form)
    datos=''
    if request.method=="POST" and reg_user.validate():
        user= reg_user.username.data
        passw = reg_user.password.data
        datos = user+'@'+passw
        success_message="Bienvenido {}".format(user)
        flash(success_message)
        
    
    
    response = make_response(render_template('cookies.html', form=reg_user))
    response.set_cookie('datos_user', datos)
    return response

@app.after_request
def after_request(response):
    print('numero3')
    return response


@app.route("/saludo")
def saludo():
    valor_cookies=request.cookies.get("datos_user")
    nombre = valor_cookies.split('@')
    return render_template('saludo.html', nom= nombre[0])

@app.route("/")
def formprueba():
    return render_template("formulario2.html")

@app.route("/Alumnos",methods=["GET","POST"])
def Alumno():
    #aqui instanciamos la clase
    #atravez de un objeto le pasamos los datos
    alum_form=forms.UserForm(request.form)
    mat=''
    nom=''
    if request.method=="POST" and alum_form.validate():
        
        mat=alum_form.matricula.data
        nom=alum_form.nombre.data
        #alum_form.apaterno.data
        #alum_form.amaterno.data
        #alum_form.email.data
        

    return render_template("Alumnos.html",form=alum_form,mat=mat,nom=nom)


@app.route("/CajasDi", methods=['GET','POST'])
def CajasDi():
    reg_caja=actividad1.CajaForm(request.form)
    if request.method=='POST':
        btn = request.form.get("btn")
        if btn == 'Cargar':
            return render_template('actividad1.html',form=reg_caja)
        if btn == 'Datos':
            numero = request.form.getlist("numeros")
            max_value = None
            for num in numero:
                if (max_value is None or num > max_value):
                    max_value = num

            min_value = None
            for num in numero:
                if (min_value is None or num < min_value):
                    min_value = num

            for i in range(len(numero)):
                numero[i] = int(numero[i])


            prom = 0
            prom = sum(numero) / len(numero)

            counter = Counter(numero)
            resultados = counter.most_common()
            textoResultado = ''
            for r in resultados:
                if r[1] > 1:
                   textoResultado += '<p>El número {0} se repite {1}</p>'.format(r[0], r[1])
            return render_template('resActividad1.html',form=reg_caja, max_value=max_value, min_value=min_value, prom=prom, repetidos = textoResultado)
    return render_template('actividad1.html', form=reg_caja)



    
@app.route('/Diccionario', methods=['GET', 'POST'])
def resistencia():
    formGuardar = actividadDic.GuardarForm(request.form)
    formBuscar = actividadDic.BuscarForm(request.form)
    result = ''

    # Si se presionó el botón de guardar
    if request.method == 'POST' and 'guardar' in request.form:
        if formGuardar.validate():
            espanolP = formGuardar.espanol.data.upper()
            inglesP = formGuardar.ingles.data.upper()

            # Guarda la información en el archivo de texto
            with open('diccionario.txt', 'a') as file:
                file.write(espanolP + '=' + inglesP + '\n')
    if request.method == 'POST' and 'limpiar' in request.form:
       return render_template('diccionario.html', formGuardar=formGuardar, formBuscar=formBuscar, result=result)
    # Si se presionó el botón de buscar
    if request.method == 'POST' and 'buscar' in request.form:
        if formBuscar.validate():
            palabraBuscar = formBuscar.palabra_buscar.data.upper()
            idioma = formBuscar.respuesta.data

            # Busca la información en el archivo de texto
            with open('diccionario.txt', 'r') as file:
                for line in file:
                    spanish, english = line.strip().split('=')
                    if idioma == 'en' and spanish == palabraBuscar:
                        result = english
                        break
                    elif idioma == 'es' and english == palabraBuscar:
                        result = spanish
                        break
                else:
                    result = 'Palabra no encontrada'
    if request.method == 'POST' and 'limpiar' in request.form:
       return render_template('diccionario.html', formGuardar=formGuardar, formBuscar=formBuscar, result=result)
    return render_template('diccionario.html', formGuardar=formGuardar, formBuscar=formBuscar, result=result)



@app.route('/resistencia', methods=['GET', 'POST'])
def index():
    formRes = forms.ResistorForm(request.form)
    colorBanda1 =""
    colorBanda2 =""
    hexaMultip = ""
    colorTolerancia =""
    valorResistencia =""
    max_valor =""
    min_valor =""
    hexaBanda1 =""
    hexaBanda2 =""
    hexaTolerancia =""

    if request.method == 'POST' and formRes.validate():
   
        colorBanda1 = formRes.band1.data
        colorBanda2 = formRes.band2.data
        colorMultiplicador = formRes.multiplier.data
        colorTolerancia = formRes.tolerance.data
      
        hexaBanda1 = app.config['BAND_COLORS'][colorBanda1]
        hexaBanda2 = app.config['BAND_COLORS'][colorBanda2]
        hexaTolerancia = app.config['TOLERANCE_COLORS'][colorTolerancia]
        hexaMultip = app.config['MULTIPLICADOR'][colorMultiplicador]


        valorResistencia = (int(colorBanda1 + colorBanda2) * 10**int(colorMultiplicador))


        valorNominal = int(colorBanda1 + colorBanda2) * 10**int(colorMultiplicador)

        if colorTolerancia == 'oro':
            valorTolerancia = 0.05
        elif colorTolerancia == 'plata':
            valorTolerancia = 0.1
        else:
            valorTolerancia = app.config['TOLERANCE_VALUES'][colorTolerancia]

        max_valor = valorNominal * (1 + valorTolerancia)
        min_valor = valorNominal * (1 - valorTolerancia)

        #response = make_response(render_template('calculadora.html', formRes=formRes, band1_color=colorBanda1, band2_color=colorBanda2, 
                       # multiplier_color=hexaMultip, tolerance_color=colorTolerancia, 
                        #resistance_value=valorResistencia, resistance_max=max_valor, resistance_min=min_valor,
                        #band1_name=hexaBanda1, band2_name=hexaBanda2, tolerance_name=hexaTolerancia))

        #response.set_cookie('resistance_value', str(valorResistencia))
        #response.set_cookie('resistance_max', str(max_valor))
        #response.set_cookie('resistance_min', str(min_valor))
        
        success_message='¡El cálculo se ha realizado con éxito!, El valor de la resistencia es {}Ω'.format(valorResistencia)
        flash(success_message)

        #return response
        
    response = make_response(render_template('calculadora.html', formRes=formRes, band1_color=colorBanda1, band2_color=colorBanda2, 
                        multiplier_color=hexaMultip, tolerance_color=colorTolerancia, 
                        resistance_value=valorResistencia, resistance_max=max_valor, resistance_min=min_valor,
                        band1_name=hexaBanda1, band2_name=hexaBanda2, tolerance_name=hexaTolerancia))

    response.set_cookie('resistance_value', str(valorResistencia))
    response.set_cookie('resistance_max', str(max_valor))
    response.set_cookie('resistance_min', str(min_valor))
    return response


if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True,port=3000)