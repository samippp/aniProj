from bs4 import BeautifulSoup
import json
import requests
import os
import time

def scrape_subpages(link):
    anime_page = requests.get(link)
    new_soup = BeautifulSoup(anime_page.text, 'html.parser')
    anime_data = new_soup.find('td', class_='borderClass')
    try:
        name = new_soup.find('h1').findChildren()[0].text
        genres_arr = anime_data.find_all('span', itemprop='genre')
        rating = anime_data.find('span', itemprop='ratingValue').text
        studios_data = anime_data.find(lambda tag: tag.name == 'span' and 'Studios' in tag.text)
        pop_data = anime_data.find(lambda tag: tag.name == 'span' and 'Popularity' in tag.text).parent.text.strip()
        popularity = pop_data[pop_data.index('#')+1:len(pop_data)]
        studios = ""
        for x in studios_data.next_siblings:
            if x.text.strip() != '' and x.text.strip() != ',':
                studios += x.text + ','
        studios = studios[0:len(studios)-1]
        
        genres = ''
        for x in genres_arr:
            genres += x.text + '/'
        genres = genres[0:len(genres)-1]

        dict = {
            'name': name,
            'genres' : genres,
            'rating' : rating,
            'studios' : studios,
            'popularity' : popularity
        }

        with open("anime_data.json","a") as outfile:
            json.dump(dict, outfile)
    except: 
        pass


def scrape_season(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    all_anime = soup.select('div[class*="seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-"]')
    
    for anime in all_anime:
        inidiv_anime = anime.select('div[class*="js-anime-type-"]')
        for x in inidiv_anime:
            img = ''
            try:
                img = x.find('img')['src']
            except:
                img = x.find('img')['data-src']
            score = x.select('div[class*="scormem-item score score-label"]')[0].text.strip()
            popularity = x.find('div', class_='scormem-item member').text.strip()
            if 'K' not in popularity:
                break
            name = x.find('a').text
            genre_data = x.find_all('span', class_='genre')
            genres = ''
            studios = ''
            for g in genre_data:
                genres += g.findChildren()[0].text +','
            try:
                themes = x.find(lambda tag: tag.name == 'span' and 'Theme' in tag.text).next_siblings
                for t in themes:
                    genres += t.text + ','
            except:
                pass
            try:
                demographic = x.find(lambda tag: tag.name == 'span' and 'Demographic' in tag.text).next_siblings
                for d in demographic:
                    genres += d.text + ','
            except:
                pass
            genres = genres[0:len(genres)-1]
            studios_data = x.find(lambda tag: tag.name == 'span' and 'Studio' in tag.text).next_siblings
            for s in studios_data:
                studios += s.text + ','
            studios = studios[0:len(studios)-1]
            dict = {
                'name' : name,
                'studios' : studios,
                'genres' : genres,
                'popularity' : popularity,
                'score' : score,
                'img' : img
            }

            with open("anime_data.json","a") as outfile:
                json.dump(dict, outfile)
        
        

if __name__ == '__main__':

    start_time = time.time()

    if os.path.exists("anime_data.json"):
        os.remove("anime_data.json")
    seasons = ['winter','spring','summer','fall']
    for i in range(2004,2025):
        for s in seasons:
            url = 'https://myanimelist.net/anime/season/'+str(i)+'/'+s
            scrape_season(url)
    
    
    
    '''scrape_subpages('https://myanimelist.net/anime/58447/Shibuya%E2%99%A1Hachi')'''

    end_time = time.time()
    total_time = end_time - start_time
    print("Execution Time: ", total_time, "seconds")
