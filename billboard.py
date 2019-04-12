import requests

from bs4 import BeautifulSoup


class Billboard:
    def __init__(self, link):
        self.link = link

    def get_page(self):
        return requests.get(self.link)

    def parse_page(self, page):
        return BeautifulSoup(page.content, 'html.parser')

    def get_tracks_from_billboard(self, soup):
        """
        Collects song titles from billboards.com
        """
        chart_name = soup.find(class_='chart-detail-header__chart-name')
        artists = soup.find_all(class_='chart-list-item__artist')
        songs = soup.find_all(class_='chart-list-item__title-text')
        
        return artists, songs, chart_name
