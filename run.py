import requests
import csv
import json
import urllib.request
import os
import time

def get_county_list():
    url = 'https://www2.census.gov/geo/docs/reference/codes/files/st42_pa_places.txt'
    response = requests.get(url)
    response.encoding = 'ISO-8859-1'

    if response.status_code == 200:
        lines = response.text.splitlines()
        reader = csv.reader(lines, delimiter='|')
        city_county_list = []
        for row in reader:
            if len(row) >= 7:
                county_name = row[6].strip()
                city_county_list.append(county_name)
        city_county_list = list(set(city_county_list))
        
        print(len(city_county_list))
        return city_county_list
    else:
        print('Unable to get the data')

def ask_response(text):
    url = "http://10.246.251.15:2025/ggmap"

    payload = json.dumps({
    "text": text
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
    return response.json()

def ask_response_view(text):
    url = "http://10.246.251.15:2026/mapview"

    payload = json.dumps({
    "text": text
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
    return response.json()

def save_pic(url,file_name):
    output_path = 'image'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    save_path = f"{output_path}/{file_name}.png"
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
            with open(save_path, 'wb') as image_file:
                image_file.write(image_data)
        print(f"img saved to {save_path}")
    except Exception as e:
        print(f"download error: {e}")


if __name__ == "__main__":
    county_list = get_county_list()
    for county in county_list:
        search_query = f"store with onsite outdoor parking in {county}"
        print(search_query)
        res = ask_response(search_query)
        print(len(res))

        with open('records.json', 'a', encoding='utf-8') as f:
            for entry in res:
                entry['county'] = county
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')

        for i in res:
            add_location = f"{i['location']['lat']},{i['location']['lng']}"
            view = ask_response_view(add_location)
            image_url = view['street_view_url']
            print(view)
            save_pic(image_url,file_name=f"{i['name']},{i['address']}")
            time.sleep(12)
        break
 
