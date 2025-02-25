import json
import urllib.error
import urllib.parse
import urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = '<API_KEY>'

@app.route('/mapview', methods=['POST'])
def get_street_view():
    data = request.json
    query = data.get('text')

    if not query:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    geocode_params = urllib.parse.urlencode({
        'address': query,
        'key': API_KEY
    })
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?{geocode_params}"

    try:
        with urllib.request.urlopen(geocode_url) as response:
            geocode_data = json.load(response)
    except urllib.error.URLError as e:
        return jsonify({"error": f"Failed to fetch geocode data: {e.reason}"}), 500

    if 'results' not in geocode_data or not geocode_data['results']:
        return jsonify({"error": "Location not found"}), 404

    location = geocode_data['results'][0]['geometry']['location']
    lat, lng = location['lat'], location['lng']

    static_map_params = urllib.parse.urlencode({
        'center': f"{lat},{lng}",
        'zoom': '19',
        'size': '600x400',
        'scale': '2',
        'maptype': 'satellite',
        'key': API_KEY
    })
    static_map_url = f"https://maps.googleapis.com/maps/api/staticmap?{static_map_params}"

    return jsonify({
        'query': query,
        'latitude': lat,
        'longitude': lng,
        'street_view_url': static_map_url
    })

if __name__ == "__main__":
    app.run(debug=False, port=2026, host="0.0.0.0")
