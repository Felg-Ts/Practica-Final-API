import os
from flask import Flask, request,url_for,render_template
from jinja2 import Template
import json

app = Flask(__name__)	

@app.route('/',methods=["GET"])
def inicio():
    return render_template("inicio.html",titulo="Inicio")

@app.route('/juegos',methods=["GET"])
def juegos():
    return render_template("juegos.html",titulo="juegos")


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