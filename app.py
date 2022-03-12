#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import requests
from prettytable import PrettyTable
from IPython import embed

parser = argparse.ArgumentParser(description="Weather API")
parser.add_argument(
    "--api-token",
    required=False,
    help="an API token from https://home.openweathermap.org/api_keys",
)
args = parser.parse_args()

if not args.api_token and "WEATHER_API_TOKEN" not in os.environ:
    message = f"""
Please create a free user account at https://openweathermap.org/api
Then create an api token at https://home.openweathermap.org/api_keys
Your API Token can be passed in via command line arguments --api-token
or loaded in your shell via WEATHER_API_TOKEN
"""
    raise Exception(message)

if args.api_token:
    token = args.api_token
else:
    token = os.environ.get("WEATHER_API_TOKEN")

SALESLOFT_LOCATIONS = [
    "Atlanta",
    "Guadalajara",
    "Indianapolis",
    "London",
    "New York",
    "San Francisco",
]

BASE_URL = "https://api.openweathermap.org"


def get_current_weather(city, token):
    url = f"{BASE_URL}/data/2.5/weather"
    params = {"q": city, "appid": token, "units": "imperial"}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to get weather data for {city=} with error message {response.json()['message']}"
        )


def get_the_weather_for_all_cities():
    data = {}
    for city in SALESLOFT_LOCATIONS:
        data[city] = get_current_weather(city, token)

    return data


def parse_weather_and_temp(city_data):
    weather = city_data["weather"][0]["main"]
    temp = city_data["main"]["temp"]
    return weather, temp


def pretty_print_weather():
    data = get_the_weather_for_all_cities()
    table = PrettyTable()
    table.field_names = ["City name", "Weather", "Temperature"]

    for city_name, city_data in data.items():
        weather, temp = parse_weather_and_temp(city_data)
        table.add_row([city_name, weather, f"{temp} F"])

    print(table)


if __name__ == "__main__":
    pretty_print_weather()
