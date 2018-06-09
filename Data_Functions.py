import requests
import csv

def params_builder(entry_ids, entry_contents):
    param_dict = {}
    for id_num, content in zip(entry_ids, entry_contents):
        param_dict[id_num] = content
    return param_dict


def post_google_form(form_url, params, backup_csv):
    with open(backup_csv, "a+", encoding='utf-8', newline='') as csv_file:
        outputwriter = csv.writer(csv_file, dialect='excel')
        values_to_write = []
        for key, value in params.items():
            values_to_write.append(value)
        outputwriter.writerow(values_to_write)

        try:
            r = requests.post(form_url, data=params, headers={"Content-type": "application/x-www-form-urlencoded"})
            return r.text
        except:
            return "Error Posting To Google"


def parse_weather_response(json_response):

    """
    JSON data to a string form used on app

    e.g. 77 °F / Broken Clouds
    """

    # Get the current temperature
    try:
        current_temp = json_response['main']['temp']
    except KeyError:
        current_temp = "?"

    try:
        current_weather = json_response['weather']
        if isinstance(current_weather, list):
            current_weather = current_weather[0]['description']
        else:
            current_weather = current_weather['description']
    except KeyError:
        current_weather = "Error Fetching Weather"

    return "{} °F / {}".format(current_temp, current_weather.title())


def fetch_weather(city_id, api_key, units='imperial'):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'id': city_id,
              'appid': api_key,
              'units': units}

    response = requests.get(base_url, params=params)
    json_response = response.json()
    weather_string = parse_weather_response(json_response)
    return weather_string

