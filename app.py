#Librerías
from flask import Flask, request,render_template,session 
import json
import requests

app = Flask(__name__)	
app.secret_key = '7r7fCCb@YVZ&3ZIHo^XImtpfC#tDmbw'

#inicio de la aplicación

@app.route('/',methods=["GET"])
def inicio():
    return render_template("inicio.html",titulo="Inicio")

#Pequeña descripción de cada programa.

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

#Formularios para los 3 programas.

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
        ruta = "/crd/acda"
        texto = "Nombre-de-una-ciudad"
        titulo2 = "Formualrio de Air Pollution API"
        getform = "tacda"
    return render_template("forms.html",titulo=titulo,titulo2=titulo2,ruta=ruta,texto=texto,getform=getform)

#Resultados de los formualarios 1 y 2.

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
            if entityName.startswith(name):
                listadatos.append(entity)

        if len(listadatos) == 0:
            return render_template("error404.html",titulo="Error404",titulo2="Error404",errormesaje="Los caracteres introducidos no coinciden con ningún nombre. Recuerde que la primera letra de la ciudad tiene que ser en mayúsculas",urlform="/forms/dma")

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
            if entityName.startswith(name):
                listadatos.append(entity)
        
        if len(listadatos) == 0:
            return render_template("error404.html",titulo="Error404",titulo2="Error404",errormesaje="Los caracteres introducidos no coinciden con ningún nombre. Recuerde que la primera letra de la ciudad tiene que ser en mayúsculas",urlform="/forms/ptdd")
        
        return render_template("ids.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos,rutaid=rutaid)

#Resultado programa 1

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

    if len(listadatos) == 0:
        return render_template("error404.html",titulo="Error404",titulo2="Error404",errormesaje="El id introducido no coincide con ninguna ciudad. Compruebe que está escrito correctamente",urlform="/forms/dma")
    
    return render_template("Current-weather-data.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos)

#Resultado programa 2-1

@app.route('/ptdd/<int:id>',methods=["GET"])
def ptdd1(id):

    listadatosptdd = []
    listadatosptdd2 = []

    session['idsession'] = id
    titulo = "5 day weather forecast"
    titulo2 = "5 day weather forecast"

    url = "https://api.openweathermap.org/data/2.5/forecast"
    querystring = {"id":f"{id}","appid":"5a74fb5df668d605eaef2012ed31eed8","units":"metric","lang":"38"}
    headers = {
        'Cache-Control': 'no-cache'
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code==200:
        datos=response.json()
        for i in datos.get("list"):
            listadatosptdd.append(i)
            for d in i["weather"]:
                listadatosptdd2.append(d)
    
    if len(listadatosptdd) == 0:
        return render_template("error404.html",titulo="Error404",titulo2="Error404",errormesaje="El id introducido no coincide con ninguna ciudad. Compruebe que está escrito correctamente",urlform="/forms/ptdd")

    return render_template("5-day-weather-forecast.html",titulo=titulo,titulo2=titulo2,listadatosptdd=listadatosptdd,listadatosptdd2=listadatosptdd2)

#Resultado programa 2-2

@app.route('/ptdd/<date>/',methods=["GET"])
def ptdd2(date):

    id = session.get("idsession", None)

    listadatosptdd = []
    listadatosptdd2 = []

    titulo = "5 day weather forecast"
    titulo2 = "5 day weather forecast"

    url = "https://api.openweathermap.org/data/2.5/forecast"
    querystring = {"id":f"{id}","appid":"5a74fb5df668d605eaef2012ed31eed8","units":"metric","lang":"38"}
    headers = {
        'Cache-Control': 'no-cache'
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code==200:
        datos=response.json()
        for i in datos.get("list"):
            if i["dt_txt"].startswith(date):
                listadatosptdd.append(i)
                for d in i["weather"]:
                    listadatosptdd2.append(d)

    if len(listadatosptdd) == 0:
        return render_template("error404.html",titulo="Error404",titulo2="Error404",errormesaje="No se ha encontrado la fecha indicada. Compruebe que está escrita correctamente",urlform="/forms/ptdd")

    return render_template("5-day-weather-forecast.html",titulo=titulo,titulo2=titulo2,listadatosptdd=listadatosptdd,listadatosptdd2=listadatosptdd2,date=date)

#Resultado formulario 3.

@app.route('/crd/acda',methods=["Post"])
def cdr():

    listadatos = []

    titulo = "Air Pollution API"
    titulo2 = "Air Pollution API"

    file = open("city.json", encoding="utf8")
    content = file.read()
    jsondecoded = json.loads(content)

    name = request.form.get("tacda")

    for entity in jsondecoded:
        entityName = entity["name"]
        if entityName.startswith(name):
            listadatos.append(entity)
    
    if len(listadatos) == 0:
        return render_template("error404.html",titulo="Error404",titulo2="Error404",errormesaje="Los caracteres introducidos no coinciden con ningún nombre. Recuerde que la primera letra de la ciudad tiene que ser en mayúsculas",urlform="/forms/acda")
    
    return render_template("crd.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos)

#Resultado programa 3.

@app.route('/acda/<lat>/<lon>',methods=["GET"])
def acda(lat, lon):

    listadatos = []

    titulo = "Air Pollution API"
    titulo2 = "Air Pollution API"

    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    querystring = {"lat":f"{lat}","lon":f"{lon}","appid":"5a74fb5df668d605eaef2012ed31eed8","units":"metric","lang":"38"}
    headers = {
        'Cache-Control': 'no-cache'
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code==200:
        datos=response.json()
        for i in datos.get("list"):
            listadatos.append(i)
    
    if len(listadatos) == 0:
        return render_template("error404.html",titulo="Error404",titulo2="Error404",errormesaje="La lon y lat no coinciden con la de ninguna ciudad. Compruebe que está escrito correctamente",urlform="/forms/acda")

    return render_template("Air-Pollution-API.html",titulo=titulo,titulo2=titulo2,listadatos=listadatos)

if __name__ == '__main__':
    app.run('0.0.0.0',int(5000), debug=True)