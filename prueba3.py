import json
import requests

file = open("city.json", encoding="utf8")
content = file.read()
jsondecoded = json.loads(content)

name = input("Dime el nombre de la ciudad: ")

for entity in jsondecoded:
    entityName = entity["name"]
    if entityName.startswith(name) is True:
        print("name: " + entity["name"], "country: " + entity["country"] , "lat:", entity["coord"]["lat"], "lon:", entity["coord"]["lon"])

print("Coordenadas")
lat = input("Dime la lat de la ciudad: ")
lon = input("Dime la lon de la ciudad: ")

url = "https://api.openweathermap.org/data/2.5/air_pollution"
querystring = {"lat":f"{lat}","lon":f"{lon}","appid":"5a74fb5df668d605eaef2012ed31eed8","units":"metric","lang":"38"}
headers = {
    'Cache-Control': 'no-cache'
    }
response = requests.request("GET", url, headers=headers, params=querystring)
if response.status_code==200:
    datos=response.json()
    print(datos)
    #for i in datos.get("list"):
    #    print(i.get("dt_txt"))
    #print(datos.get("sys").get("country"))
    #print(datos.get("main").get("temp_max"))
    #print(datos.get("main").get("temp_min"))
    #print(datos.get("main").get("humidity"))
    #print(datos.get("wind").get("speed"))

