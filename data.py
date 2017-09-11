# encoding=utf-8
import codecs
import requests
import re
from bs4 import BeautifulSoup

DOUBAN_URL = 'https://movie.douban.com/top250'

def download_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html, "lxml")
    movie_list_soup = soup.find('ol', attrs={'class':'grid_view'})

    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class':'info'})
        movie_name = detail.find('div', attrs={'class':'hd'}).find('span', attrs={'class':'title'}).getText()
        star = detail.find('div',attrs={'class':'bd'}).find('span',attrs={'class':'rating_num'}).getText()
        country_str = detail.find('div',attrs={'class':'bd'}).find_all('p')[0].getText()
        pattern = re.compile(r'/\xa0(.*)\xa0/')
        country = pattern.findall(country_str)[0]
        movie_name_list.append(movie_name + ' ' + country + ' ' + star)

    next_page = soup.find('span', attrs={'class':'next'}).find('a')

    if next_page:
        return movie_name_list, DOUBAN_URL + next_page['href']
    return movie_name_list,None


def main():
    url = DOUBAN_URL
    with codecs.open('movies.txt','wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))

if __name__ == '__main__':
    main()
