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
        ruta = "/ids/dma"
        texto = "Nombre-de-una-ciudad"
        titulo2 = "Formulario de Current weather data"
        getform = "tdma"
    elif appd == "ptdd":
        titulo = "Formulario de 5 day weather forecast"
        ruta = "/ids/ptdd"
        texto = "Nombre-de-una-ciudad"
        titulo2 = "Formulario de 5 day weather forecast"
        getform = "tptdd"
    elif appd == "acda":
        titulo = "Formulario de Air Pollution API"
        ruta = "/ids/acda"
        texto = "Nombre-de-una-ciudad"
        titulo2 = "Formualrio de Air Pollution API"
        getform = "tacda"
    return render_template("forms.html",titulo=titulo,titulo2=titulo2,ruta=ruta,texto=texto,getform=getform)

@app.route('/ids/<appd>',methods=["Post"])
def ids(appd):

    if appd == "dma":

        listadatos = []

        rutaid = "/dma/"
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
        return render_template("ids.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos,rutaid=rutaid)

    elif appd == "ptdd":

        listadatos = []

        rutaid = "/ptdd/"
        titulo = "5 day weather forecast"
        titulo2 = "5 day weather forecast"

        file = open("city.json", encoding="utf8")
        content = file.read()
        jsondecoded = json.loads(content)

        name = request.form.get("tptdd")

        for entity in jsondecoded:
            entityName = entity["name"]
            if entityName.startswith(name) is True:
                listadatos.append(entity)
        return render_template("ids.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos,rutaid=rutaid)

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
    return render_template("Current-weather-data.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos)

@app.route('/ptdd/<int:id>',methods=["GET"])
def ptdd1(id):

    listadatos = []
    listadatos2 = []


    titulo = "Current weather data"
    titulo2 = "Current weather data"

    url = "https://api.openweathermap.org/data/2.5/forecast"
    querystring = {"id":f"{id}","appid":"5a74fb5df668d605eaef2012ed31eed8","units":"metric","lang":"38"}
    headers = {
        'Cache-Control': 'no-cache'
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code==200:
        datos=response.json()
        for i in datos.get("list"):
            listadatos.append(i)
            for d in i["weather"]:
                listadatos2.append(d)
    return render_template("5-day-weather-forecast.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos,listadatos2=listadatos2)


if __name__ == '__main__':
    app.run('0.0.0.0',int(5000), debug=True)