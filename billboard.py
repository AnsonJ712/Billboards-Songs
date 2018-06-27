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
        artists = soup.find_all(class_='chart-row__artist')
        songs = soup.find_all(class_='chart-row__song')
        return artists, songs
