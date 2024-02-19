
import requests
import pytankerkoenig
from flask import Flask
from flask import request
from flask import render_template

# Adresse in Lat und Lon übersetzen
def get_coordinates(address):
    while True:
        API_ENDPOINT = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
        response = requests.get(API_ENDPOINT)
        data = response.json()
        if data:
            lat, lon = (data[0]["lat"], data[0]["lon"])
            return True, lat, lon
        else:
            return False, "49.453872", "11.077298"

# Internetseite bereitstellen
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def start():
    address = "Nürnberg"
    distance = "10"
    if request.method == "POST":
        address = request.form["address"]
        distance = request.form["distance"]

    success, latitude, longitude = get_coordinates(address)


    data = pytankerkoenig.getNearbyStations('3776ce9c-a245-4fe1-6e13-76e69be761d9', latitude, longitude, distance, 'all', 'dist')
    stations = data["stations"]
    if not stations:
        data = pytankerkoenig.getNearbyStations('3776ce9c-a245-4fe1-6e13-76e69be761d9', "49.453872", "11.077298", "100", 'all', 'dist')
        stations = data["stations"]
        success = False

    for i in range(3):
        if len(stations[i]["brand"]) > 5:
            stations[i]["brand"] = stations[i]["brand"][:5]
        brand = str(stations[i]["brand"])
        brand = brand.capitalize()
        stations[i]["brand"] = brand

    for i in range(3):
        street = str(stations[i]["street"])
        street = street.capitalize().replace("Strasse", "Str.").replace(" Straße", "Str.").replace("straße", "str.").replace("strasse", "str.")
        stations[i]["street"] = street

    for i in range(3):
        place = str(stations[i]["place"])
        place = place.capitalize()
        stations[i]["place"] = place

    return render_template("Spritpreise.html", station0=stations[0], station1=stations[1], station2=stations[2], error=not success)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.2", use_reloader=False)
