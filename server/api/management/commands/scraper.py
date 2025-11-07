from bs4 import BeautifulSoup
import json
import requests
import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings

DATA_DIR = os.path.join(settings.BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_DIR, "anime_data.json")

class Command(BaseCommand):

    def find_genres(self):
        page = requests.get("https://myanimelist.net/anime.php")
        soup = BeautifulSoup(page.text,'html.parser')
        genres = soup.find_all('div', class_='genre-list al')
        l = {}
        for g in genres:
            l[(g.text[0:g.text.index('(')]).strip()] = 0
            if 'Shounen' in g.text:
                break
        print(l)
        
    def scrape_season(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        print(page.status_code)
        animeArr = {}
        all_anime = soup.select('div[class*="seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-"]')
        for anime in all_anime:
            inidiv_anime = anime.select('div[class*="js-anime-type-"]')
            for x in inidiv_anime:
                try:
                    img = ''
                    try:
                        img = x.find('img')['src']
                    except:
                        img = x.find('img')['data-src']
                    score = x.select('div[class*="scormem-item score score-label"]')[0].text.strip()
                    if 'N/A' in score:
                        score = 0
                    popularity = x.find('div', class_='scormem-item member').text.strip()
                    if 'K' in popularity:
                        popularity = int(float(popularity[0:len(popularity)-1]) * 1000)
                    elif 'M' in popularity:
                        popularity = int(float(popularity[0:len(popularity)-1]) * 1000000)
                    elif 'N/A' in popularity:
                        popularity = None
                    else:
                        popularity = int(popularity)
                    name = x.find('a').text.encode("utf-8").decode()
                    genre_data = x.find_all('span', class_='genre')
                    genres = []
                    studios = []
                    for g in genre_data:
                        genres.append(g.findChildren()[0].text)
                    try:
                        themes = x.find(lambda tag: tag.name == 'span' and 'Theme' in tag.text).next_siblings
                        for t in themes:
                            genres.append(t.text)
                    except:
                        pass
                    try:
                        demographic = x.find(lambda tag: tag.name == 'span' and 'Demographic' in tag.text).next_siblings
                        for d in demographic:
                            genres.append(d.text)
                    except:
                        pass
                    studios_data = x.find(lambda tag: tag.name == 'span' and 'Studio' in tag.text).next_siblings
                    for s in studios_data:
                        studios.append(s.text)
                    desc = x.find('p', class_='preline').text
                    d = {
                        'name' : name,
                        'desc' : desc,
                        'studios' : studios,
                        'genres' : genres,
                        'popularity' : popularity,
                        'score' : float(score),
                        'img' : img
                    }
                    animeArr[name] = d
                    '''with open("anime_data.json","a") as outfile:
                        outfile.write(json.dumps(dict, indent=4))
                        outfile.write(",\n")'''
                except:
                    pass
        return animeArr

    def handle(self, *args, **options):
        start_time = time.time()
        
        if os.path.exists("anime_data.json"):
            os.remove("anime_data.json")
        seasons = ['winter','spring','summer','fall']
        animeArr = {}
        for i in range(2004,2025):
            for s in seasons:
                url = 'https://myanimelist.net/anime/season/'+str(i)+'/'+s
                print(s+' ' + str(i) + ' / ',end='')
                animeArr.update(self.scrape_season(url))
        animeArr = list(animeArr.values())
        with open(OUTPUT_FILE,"w") as file:
            json.dump(animeArr,file)
        
        end_time = time.time()
        total_time = end_time - start_time
        print("Execution Time: ", total_time, "seconds")
