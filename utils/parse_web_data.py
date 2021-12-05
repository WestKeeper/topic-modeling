import argparse
import requests as req
from pathlib import Path
import os
import sys
import time
from transliterate import translit

from bs4 import BeautifulSoup

ROOT_DIR = Path(os.getcwd()).resolve()
if ROOT_DIR not in sys.path:
    sys.path.append(str(ROOT_DIR))

from resourses.resourses import KINOPOISK_MAIN
from resourses.resourses import KINOPOISK_PAGES


TO_PRINT = False
TO_SAVE = True

KINOPOISK_BEST_250_MOVIES_PAGES = [
    'https://www.kinopoisk.ru/lists/top250/',
    'https://www.kinopoisk.ru/lists/top250/?page=2&tab=all',
    'https://www.kinopoisk.ru/lists/top250/?page=3&tab=all',
    'https://www.kinopoisk.ru/lists/top250/?page=4&tab=all',
    'https://www.kinopoisk.ru/lists/top250/?page=5&tab=all',
]

GOOGLE_CASH_BASE = 'http://webcache.googleusercontent.com/search?q=cache:'


def get_250_best_movies():
    save_path = ROOT_DIR / Path(f'data/kinopoisk/meta')
    save_path.mkdir(parents=True, exist_ok=True)
    filepath = save_path / Path('best-250-films.txt')
    open(filepath, 'w').close()
    
    for best_250_movies_page in KINOPOISK_BEST_250_MOVIES_PAGES:
        resp = req.get(f'{GOOGLE_CASH_BASE}{best_250_movies_page}')
        soup = BeautifulSoup(resp.text, 'lxml')
        film_names = soup.find_all('p', {'class': 'selection-film-item-meta__name'})

        with filepath.open('a', encoding='utf-8') as fout:
            for film_name in film_names:
                fout.write(film_name.get_text(' ', strip=True))
                fout.write('\n')


def parse_kinopoisk_film(page_url: str, to_save: bool):
    if page_url[-1] != '/':
        page_url += '/'
    resp = req.get(f'{GOOGLE_CASH_BASE}{page_url}')
    soup = BeautifulSoup(resp.text, 'lxml')
    
    titles = soup.find_all('a', {'class': 'breadcrumbs__link'})
    print(f'{GOOGLE_CASH_BASE}{page_url}')
    print(titles)
    
    title = titles[0].get_text().replace(' ', '-')
    eng_title = title.translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/kinopoisk/{eng_title}')
    save_path.mkdir(parents=True, exist_ok=True)

    reviews = soup.find_all('span', {'class': '_reachbanner_'})
    for i, review in enumerate(reviews):
        review_text = review.get_text(' ', strip=True)
        filepath = save_path / Path(f'{i}.txt')
        with filepath.open('w', encoding='utf-8') as fout:
            fout.write(review_text)
        
        if TO_PRINT:
            print(review_text)

def main():
    """Main parsing method."""
    for best_250_movies_page in KINOPOISK_BEST_250_MOVIES_PAGES: 
        resp = req.get(f'{GOOGLE_CASH_BASE}{best_250_movies_page}')
        soup = BeautifulSoup(resp.text, 'lxml')
        film_names = soup.find_all('a', {'class': 'selection-film-item-meta__link'}, href=True) # TODO: узнать про 250 ids фильмов, использовать неофициальную api
        print(f'{best_250_movies_page}')
        print(resp.text)
        for film_name in film_names:
            review_url = 'https://www.kinopoisk.ru' + film_name['href'] + 'reviews'
            print(review_url)
            parse_kinopoisk_film(review_url, to_save=TO_SAVE)

            time.sleep(1)



if __name__ == '__main__':
    main()
    # get_250_best_movies()
