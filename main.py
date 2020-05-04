from bs4 import BeautifulSoup
import requests
import json
import time
from tqdm import tqdm

getData = False
getCityData = True
getCountryData = True

if getData:
    # Get Countries
    r = requests.get("https://wikitravel.org/en/A%E2%80%93Z_list_of_countries")
    soup = BeautifulSoup(r.content, 'html.parser')

    countries = []

    for x in soup.find_all('li'):
        try:
            x['id']
        except:
            try:
                if x['class'] == "new":
                    countries.append(str(x.decode_contents()))
            except:
                countries.append(str(x.decode_contents()))

    output = {}
    output['countries'] = []
    for x in range(0,len(countries)-1):
        output['countries'].append({
            "link": "https://wikitravel.org" + countries[x].split('"')[1],
            "name": countries[x].split("</a")[0].split('">')[1]
        })

    with open("countries.json", "w+") as out:
        json.dump(output, out, indent=4)

    # Get Cities
    r = requests.get("https://wikitravel.org/en/Wikitravel:World_cities")
    soup = BeautifulSoup(r.content, 'html.parser')

    cities = []

    for x in soup.find_all('li'):
        try:
            x['id']
        except:
            try:
                if x['class'] == "new":
                    cities.append(str(x.decode_contents()))
            except:
                cities.append(str(x.decode_contents()))

    output = {}
    output['cities'] = []
    for x in range(0,len(cities)):
        output['cities'].append({
            "link": "https://wikitravel.org" + cities[x].split('"')[1],
            "name": cities[x].split("</a")[0].split('">')[1]
        })

    with open("cities.json", "w+") as out:
        json.dump(output, out, indent=4)


if getCityData:
    with open("cities.json", 'r') as inp:
        cities = json.loads(inp.read())['cities']
        
        with open("cities.csv", 'w+', encoding='utf-8') as out:
            out.write("City,Source Link,Paragraph Content\n")
            print('cities')
            for i in tqdm(range(0,len(cities))):
                try:
                    r = requests.get(cities[i]['link'])
                    soup = BeautifulSoup(r.content, 'html.parser')

                    for p in soup.find_all('p'):
                        if "tap" in p.text.strip().lower() and "water" in p.text.strip().lower():
                            try:
                                out.write(cities[i]['name'] + "," + cities[i]['link'] + "," + p.text.strip().replace("\n", "").replace(",", "%2C") + "\n")
                            except:
                                continue
                except:
                    continue

                time.sleep(2)


if getCountryData:
    with open("countries.json", 'r') as inp:
        countries = json.loads(inp.read())['countries']
        
        with open("countries.csv", 'w+', encoding='utf-8') as out:
            out.write("Country,Source Link,Paragraph Content\n")

            for i in tqdm(range(0,len(countries))):
                try:
                    r = requests.get(countries[i]['link'])
                    soup = BeautifulSoup(r.content, 'html.parser')

                    for p in soup.find_all('p'):
                        if "tap" in p.text.strip().lower() and "water" in p.text.strip().lower():
                            try:
                                out.write(countries[i]['name'] + "," + countries[i]['link'] + "," + p.text.strip().replace("\n", "").replace(",", "%2C") + "\n")
                            except:
                                continue
                except:
                    continue

                time.sleep(2)