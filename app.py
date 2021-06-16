import os
from flask import Flask, request,url_for,render_template
from jinja2 import Template
import json

app = Flask(__name__)	

@app.route('/',methods=["GET"])
def inicio():
    return render_template("inicio.html",titulo="Inicio")

@app.route('/detalles/<appd>/',methods=["GET"])
def detalles(appd):
    if appd == "dma":
        titulo = "Detalles de Current weather data"
        detalle = "Acceda a los datos meteorológicos actuales de cualquier lugar de la Tierra, incluidas más de 200.000 ciudades."
        titulo2 = "Detalles de Current weather data"
    elif appd == "ptdd":
        titulo = "Detalles de 5 day weather forecast"
        detalle = "El pronóstico de 5 días está disponible en cualquier lugar o ciudad. Incluye datos de pronóstico del tiempo con pasos de 3 horas."
        titulo2 = "Detalles de 5 day weather forecast"
    elif appd == "acda":
        titulo = "Detalles Air Pollution API"
        detalle = "Esta herramienta proporciona datos de contaminación del aire actuales, pronosticados e históricos para cualquier coordenada del mundo."
        titulo2 = "Detalles Air Pollution API"
    return render_template("detalles.html",appd=appd, titulo=titulo,detalle=detalle,titulo2=titulo2)


@app.route('/listajuegos',methods=["POST"])
def listajuegos():
    
    l1 = []

    f = open("MSX.json", "r")
    content = f.read()
    jsondecoded = json.loads(content)

    nombrej=request.form.get("tjuego")

    for i in jsondecoded:
        entityName = i["nombre"]
        if entityName.startswith(nombrej):
            l1.append(i)
    if len(l1) == 0:
        error = "No se encontró ninguna coincidencia con los caracteres introducidos"
        return render_template("error404.html",titulo="error404", error=error)


    return render_template("listajuegos.html",titulo="listajuegos", l1=l1)

@app.route('/juego/<int:id>/',methods=["GET","POST"])
def juego(id):

    l1 = []

    f = open("MSX.json", "r")
    content = f.read()
    jsondecoded = json.loads(content)

    for i in jsondecoded:
        entityid = i["id"]
        if entityid == id:
            l1.append(i)
    if len(l1) == 0:
        error = "No se encontró ninguna coincidencia con el id introducido"
        return render_template("error404.html",titulo="error404", error=error)

    return render_template("juego.html",titulo="juego", l1=l1)

if __name__ == '__main__':
    app.run('0.0.0.0',int(5000), debug=True)