from flask import request, make_response, render_template, flash
from flask.views import MethodView
from forms import ResistorForm

class Resistencia(MethodView):
    def get(self):
        formRes = ResistorForm()
        return render_template('calculadora.html', formRes=formRes)

    def post(self):
        formRes = ResistorForm(request.form)
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

        if formRes.validate():
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

            success_message='¡El cálculo se ha realizado con éxito!, El valor de la resistencia es {}Ω'.format(valorResistencia)
            flash(success_message)

        response = make_response(render_template('calculadora.html', formRes=formRes, band1_color=colorBanda1, band2_color=colorBanda2, 
                            multiplier_color=hexaMultip, tolerance_color=colorTolerancia, 
                            resistance_value=valorResistencia, resistance_max=max_valor, resistance_min=min_valor,
                            band1_name=hexaBanda1, band2_name=hexaBanda2, tolerance_name=hexaTolerancia))

        response.set_cookie('resistance_value', str(valorResistencia))
        response.set_cookie('resistance_max', str(max_valor))
        response.set_cookie('resistance_min', str(min_valor))
        return response
