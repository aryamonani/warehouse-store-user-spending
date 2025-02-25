import os
from google.cloud import texttospeech
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/ggmap', methods=['post'])
def t2s():
    output = {}
    data = request.json
    print('Get request:')
    print(data)

    QUERY = data.get('text')
    API_KEY ='<API_KEY>'
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={QUERY}&key={API_KEY}"

    all_places = []
    output = []
    while url:
        response = requests.get(url)
        data = response.json()
        if "results" in data:
            all_places.extend(data["results"])
        
        if "next_page_token" in data:
            next_page_token = data["next_page_token"]
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}&key={API_KEY}"
        else:
            url = None

    for place in all_places:
        js = {}
        js['name'] = place['name']
        js['address'] = place['formatted_address']
        js['location'] = place['geometry']['location']
        js['place_id'] = place['place_id']
        output.append(js)

    print(len(output))
    # return output,all_places
    return output

if __name__ == "__main__":
    app.run(debug=False, port=2025, host='0.0.0.0')