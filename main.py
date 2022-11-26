from fastapi import FastAPI
import urllib.request, json
import random
import requests


app = FastAPI()

user_num = random.randint(5, 20)

class Country:
    def __init__(self, name, capital, population, languages):
        self.name = name
        self.capital = capital
        self.population = population
        self.languages = languages



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/countries")
async def get_address():
    list_countries = []
    with urllib.request.urlopen("https://random-data-api.com/api/v2/addresses?size="+f"{user_num}") as url:
        data = json.load(url)
    for country_num in range(user_num):
        list_countries.append(data[country_num]["country"])

    print(list_countries)
    requested_countries = {}
    for i in range(len(list_countries)):
        country = list_countries[i].replace(" ", "")
        url_country = "https://restcountries.com/v3.1/name/"+f"{country}"
        if requests.get(url_country).status_code == 404:
            requested_countries[country] = "No information found!"
        else:
            with urllib.request.urlopen(url_country) as url:
                data = json.load(url)
            country1 = Country(data[0]["name"]["official"], data[0]["capital"], data[0]["population"], data[0]["languages"])
            requested_countries[country] = country1.__dict__
    return requested_countries

