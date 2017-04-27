import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.billboard.com/charts/hot-100")

soup = BeautifulSoup(page.content, 'html.parser')

artists = soup.find_all(class_='chart-row__artist')
songs = soup.find_all(class_='chart-row__song')

for x in range(0,9):
    print(songs[x].get_text().strip() + " - " + artists[x].get_text().strip())


