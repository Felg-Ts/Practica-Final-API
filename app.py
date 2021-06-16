from flask import Flask, request,url_for,render_template
from jinja2 import Template
import json
import requests

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
        titulo = "Detalles de Air Pollution API"
        detalle = "Esta herramienta proporciona datos de contaminación del aire actuales, pronosticados e históricos para cualquier coordenada del mundo."
        titulo2 = "Detalles Air Pollution API"
    return render_template("detalles.html",appd=appd,titulo=titulo,detalle=detalle,titulo2=titulo2)

@app.route('/forms/<appd>',methods=["GET"])
def forms(appd):
    if appd == "dma":
        titulo = "Formulario de Current weather data"
        ruta = "/dma"
        texto = "Nombre-de-una-ciudad"
        titulo2 = "Formulario de Current weather data"
        getform = "tdma"
    elif appd == "ptdd":
        titulo = "Formulario de 5 day weather forecast"
        ruta = "/ptdd"
        texto = "Nombre-de-una-ciudad"
        titulo2 = "Formulario de 5 day weather forecast"
        getform = "tptdd"
    elif appd == "acda":
        titulo = "Formulario de Air Pollution API"
        ruta = "/acda"
        texto = "Nombre-de-una-ciudad"
        titulo2 = "Formualrio de Air Pollution API"
        getform = "tacda"
    return render_template("forms.html",titulo=titulo,titulo2=titulo2,ruta=ruta,texto=texto,getform=getform)

@app.route('/dma',methods=["Post"])
def ids():

    listadatos = []

    titulo = "Current weather data"
    titulo2 = "Current weather data"

    file = open("city.json", encoding="utf8")
    content = file.read()
    jsondecoded = json.loads(content)

    name = request.form.get("tdma")

    for entity in jsondecoded:
        entityName = entity["name"]
        if entityName.startswith(name) is True:
            listadatos.append(entity)
    return render_template("ids.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos)

@app.route('/dma/<int:id>',methods=["GET"])
def dma(id):

    listadatos = []

    titulo = "Current weather data"
    titulo2 = "Current weather data"

    url = "https://api.openweathermap.org/data/2.5/weather"
    querystring = {"id":f"{id}","appid":"5a74fb5df668d605eaef2012ed31eed8","units":"metric","lang":"38"}
    headers = {
        'Cache-Control': 'no-cache'
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code==200:
        datos=response.json()
        listadatos.append(datos)
    return render_template("Current-weather-data.html",titulo=titulo,titulo2=titulo2, listadatos=listadatos)

if __name__ == '__main__':
    app.run('0.0.0.0',int(5000), debug=True)