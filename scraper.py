from bs4 import BeautifulSoup
import requests

url = "https://myanimelist.net/anime/season"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
all_anime = soup.find_all('div', class_='seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1')
print(all_anime)