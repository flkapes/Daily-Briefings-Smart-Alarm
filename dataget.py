"""
This file contaons three main functions, get_covid_json, weather, and news.
The function weather is responsible for calling a weather API and storing
the response, and then extracts the data so it may be imported from the app.py
module.
The news function calls the newsapi api and saves the results to a json file.
The covid function uses the uk_covid19 SDK from Public Health England and saves
the data in a json file.
"""

import json
import requests
from uk_covid19 import Cov19API


def weather_test():
    """
    This function is responsible for testing and checking the response of the
    weather API, it will return the response code as an integer. This is part
    of the pytest functionality.
    """
    with open('config.json', 'r') as conf:
        conf = json.load(conf)
        # Gets the API key from the config.json file
        weather_api_key = conf["weather_api_key"]
        weather_city_name = conf['weather_city_name']
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?'
            'q=' +
            weather_city_name +
            '&units=metric&appid=' +
            weather_api_key)
        response_code = response.status_code
        return response_code


def news_test():
    """
    This function is responsible for testing and checking the response of the
    news API, it will return the response code as an integer. This is part
    of the pytest functionality.
    """
    with open('config.json', 'r') as cfile:
        config = json.load(cfile)
        news_api_key = config["news_api_key"]
        response = requests.get("https://newsapi.org/v2/top-headlines?"
                                "sources=bbc-news&apiKey=" + news_api_key)
        response_code = response.status_code
        return response_code


def weather():
    """
    This function is responsible for weather data. There are two functions
    nested within it, weather_api_call, and weather_data_extractor.
    In weather_api_call the requests module is used to call the OpenWeatherMap
    API.The API key, and requested city are taken from the config.json file.
    This function returns nothing. The weather_data_extractor takes the
    relevant data from the weather.json file and returns three vaalues,
    the current temperature, what it currently feels like, and a one-two
    word description of the weather.
    """
    def weather_api_call():
        with open('config.json', 'r') as conf:
            conf = json.load(conf)
            # Gets the API key from the config.json file
            weather_api_key = conf["weather_api_key"]
            weather_city_name = conf['weather_city_name']
            response = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?'
                'q=' + weather_city_name + '&units=metric&appid=' + weather_api_key)
            resp_json = response.json()
            with open('weather.json', 'w') as outfile:
                # Uses the data from the API to overwrite the weather data
                json.dump(resp_json, outfile)
                outfile.close()

    def weather_data_extractor():
        with open('weather.json', 'r') as weather_json:
            weather_json = json.load(weather_json)
            temp = weather_json["main"]
            weather_item = weather_json["weather"]
            desc = weather_item[0]
            current_temperature = "The current temperature is: " + \
                str(int(temp["temp"])) + "C"
            current_feels_like = "Feels like: " + \
                str(int(temp["feels_like"])) + "C"
            forecast = desc["main"]
            return current_feels_like, current_temperature, forecast

    weather_api_call()
    return weather_data_extractor()


def news():
    """
    The news function here also utilizes the requests module in order to call
    the NewsAPI API for top headlines. The API key is also derived from the
    config.json file. The data the API returns is added to the news.json file.
    """
    with open('config.json', 'r') as cfile:
        config = json.load(cfile)
        news_api_key = config["news_api_key"]
        response = requests.get("https://newsapi.org/v2/top-headlines?"
                                "sources=bbc-news&apiKey=" + news_api_key)
        resp_json = response.json()
        with open("news.json", 'w') as file:
            json.dump(resp_json, file)
            file.close()


def get_national_covid_json():
    """
    This function uses the uk_covid19 module provided by Public Health England.
    The function uses the config.json file to set the areaType and areaName,
    and default values are set to the nation of England. The API returns a list
    of dictionaries with four metrics, new cases, total cases, new deaths,
    and total deaths. All of this is saved to a file named covid.json.
    """
    with open('config.json', 'r') as file:
        file2 = json.load(file)
        covid_area_type = file2['covid_area_type']
        covid_area_name = file2['covid_area_name']
    area_info = [
        'areaType=' + covid_area_type,
        'areaName=' + covid_area_name
    ]
    total_and_new_cases_deaths = {
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }
    api_return = Cov19API(
        filters=area_info,
        structure=total_and_new_cases_deaths)
    covid_resp_json = api_return.get_json(save_as='covid.json')
    return covid_resp_json
