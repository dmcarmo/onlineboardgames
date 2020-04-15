import time

from bs4 import BeautifulSoup
import requests

class Timeout:
    @staticmethod
    def timeout(func):
            def wrapper(*args, **kwargs):
                    end_time = time.time()
                    diff_time = Timeout.delay - (end_time - Timeout.start_time)
                    time.sleep(max(0,diff_time))
                    Timeout.start_time = time.time()
                    return func(*args, **kwargs)
            return wrapper
    delay = 2
    start_time = 0

@Timeout.timeout
def request(params, headers):
    r = requests.get('https://tabletopia.com/games?', params, headers=headers)
    r.raise_for_status()    # HTTP request error check
    return r

def load_soup(file):
    return BeautifulSoup(file, 'html.parser')

def get_last_page(soup):
    return soup.find_all('a', {'class': 'pagination-link'})[-2].text

def download_all_pages():
    headers = {'Referer': 'https://tabletopia.com/games?',
	       'X-Requested-With': 'XMLHttpRequest'}
    games = request({}, headers=headers)
    request_list = [games.text]
    soup = load_soup(games.text)
    last_page = int(get_last_page(soup))
    for page in range(2, 1+last_page):
        headers = {'Referer': f"https://tabletopia.com/games?page={page}",
                   'X-Requested-With': 'XMLHttpRequest'}
        games = request({'page':page}, headers)
        request_list.append(games.text)
    return request_list

def parser(text):
    def get_games_list(soup):
        return soup.find_all('div', {'class': 'item__bottom _more-offset'})
    soup = load_soup(text)
    game_list = get_games_list(soup)
    return {item.h3.text: item.a['href'] for item in game_list}

def url_maker(value):
    return f"https://tabletopia.com{value}"

def main():
    request_list = download_all_pages()
    return {data: url_maker(dict_[data]) for dict_ in [parser(text) for text in request_list] for data in dict_}
