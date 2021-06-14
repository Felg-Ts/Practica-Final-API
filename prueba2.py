import json
import requests
from requests.api import get

file = open("city.json", encoding="utf8")
content = file.read()
jsondecoded = json.loads(content)

name = input("Dime el nombre de la ciudad: ")

for entity in jsondecoded:
    entityName = entity["name"]
    if entityName.startswith(name) is True:
        print("name: " + entity["name"], "country: " + entity["country"] , "id:",  entity["id"])

id = input("Dime el id de la ciudad: ")

url = "https://api.openweathermap.org/data/2.5/forecast"
querystring = {"id":f"{id}","appid":"5a74fb5df668d605eaef2012ed31eed8","units":"metric","lang":"38"}
headers = {
    'Cache-Control': 'no-cache'
    }
response = requests.request("GET", url, headers=headers, params=querystring)
if response.status_code==200:
    datos=response.json()
    #print(datos)
    for i in datos.get("list"):
        print(i.get("dt_txt"))

    date = input("Indique la fecha y hora que quiere comprobar: ")    
    for x in datos.get("list"):
        if x["dt_txt"] == date:
            for x1 in x["weather"]:
                print(x1.get("description"))
            print(x.get("main").get("temp_max"))
            print(x.get("main").get("temp_min"))
            print(x.get("main").get("humidity"))
            print(x.get("wind").get("speed"))

