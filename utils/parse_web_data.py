import argparse
import requests as req
from pathlib import Path
import os
import sys
import time

from transliterate import translit
from bs4 import BeautifulSoup

ROOT_DIR = Path(os.getcwd()).resolve().parent
if ROOT_DIR not in sys.path:
    sys.path.append(str(ROOT_DIR))

from resourses.resourses import KINOPOISK_MAIN
from resourses.resourses import KINOPOISK_PAGES


TO_PRINT = False
TO_SAVE = True
TO_PARSE_KINOPOISK = False
TO_PARSE_RECEIPTS = False
TO_PARSE_POLITICS = False
PARSE_FROM_RBC_POLITICS_MAIN = False
TO_PARSE_WIKI_HOW = False
PARSE_FROM_WIKI_HOW_MAIN= False
TO_PARSE_PSYCHOJOURNAL = False
TO_PARSE_TEXTERRA = False
TO_PARSE_RUSSIADISCOVERY = False
TO_PARSE_VANDROUKI = False
TO_PARSE_FREE_WRITER = True

TO_USE_GOOGLE_CASH = False

KINOPOISK_BEST_250_MOVIES_PAGES = [
    'https://www.kinopoisk.ru/lists/top250/',
    'https://www.kinopoisk.ru/lists/top250/?page=2&tab=all',
    'https://www.kinopoisk.ru/lists/top250/?page=3&tab=all',
    'https://www.kinopoisk.ru/lists/top250/?page=4&tab=all',
    'https://www.kinopoisk.ru/lists/top250/?page=5&tab=all',
]

POVARENOK_RECEIPTS_PAGES = [
    'https://www.povarenok.ru/recipes/',
    'https://www.povarenok.ru/recipes/~2/',
    'https://www.povarenok.ru/recipes/~3/',
    'https://www.povarenok.ru/recipes/~4/',
    'https://www.povarenok.ru/recipes/~5/',
    'https://www.povarenok.ru/recipes/~6/',
    'https://www.povarenok.ru/recipes/~7/',
    'https://www.povarenok.ru/recipes/~8/',
    'https://www.povarenok.ru/recipes/~9/',
    'https://www.povarenok.ru/recipes/~10/',
]

RBC_POLITICS_PAGE = 'https://www.rbc.ru/politics/'

RBC_POLITICS_QUERY_PAGES = [
    'https://www.rbc.ru/search/?category=TopRbcRu_politics&dateFrom=02.11.2021&dateTo=01.12.2021',
    'https://www.rbc.ru/search/?category=TopRbcRu_politics&dateFrom=02.10.2021&dateTo=01.11.2021',
    'https://www.rbc.ru/search/?category=TopRbcRu_politics&dateFrom=02.09.2021&dateTo=01.10.2021',
    'https://www.rbc.ru/search/?category=TopRbcRu_politics&dateFrom=02.08.2021&dateTo=01.09.2021',
    'https://www.rbc.ru/search/?category=TopRbcRu_politics&dateFrom=02.07.2021&dateTo=01.08.2021',
]

WIKI_HOW_PAGE_MAIN = 'https://ru.wikihow.com/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F-%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'

WIKI_HOW_CATEGORY_PAGES = [
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%BE-%D0%B8-%D1%80%D0%B0%D0%B7%D0%B2%D0%BB%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D1%8F',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D1%8B-%D0%B8-%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%B8%D0%BA%D0%B0',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A1%D0%B5%D0%BC%D0%B5%D0%B9%D0%BD%D0%B0%D1%8F-%D0%B6%D0%B8%D0%B7%D0%BD%D1%8C',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D1%8B-%D0%B8-%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D1%83%D0%BB%D0%B8%D0%BD%D0%B0%D1%80%D0%B8%D1%8F-%D0%B8-%D0%B3%D0%BE%D1%81%D1%82%D0%B5%D0%BF%D1%80%D0%B8%D0%B8%D0%BC%D1%81%D1%82%D0%B2%D0%BE',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%97%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%D1%8C%D0%B5',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D0%B8%D1%8F-%D0%B8-%D1%80%D0%B5%D0%BB%D0%B8%D0%B3%D0%B8%D1%8F',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%83%D1%82%D0%B5%D1%88%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%8F',
    'https://ru.wikihow.com/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9C%D0%BE%D0%BB%D0%BE%D0%B4%D0%B5%D0%B6%D1%8C',
]

PSYCHOJOURNAL_PAGES = [
    'https://psychojournal.ru/article',
    'https://psychojournal.ru/article/page/2/',
    'https://psychojournal.ru/article/page/3/',
    'https://psychojournal.ru/article/page/4/',
    'https://psychojournal.ru/article/page/5/',
    'https://psychojournal.ru/article/page/6/',
    'https://psychojournal.ru/article/page/7/',
    'https://psychojournal.ru/article/page/8/',
    'https://psychojournal.ru/article/page/9/',
    'https://psychojournal.ru/article/page/10/',
]

TEXTERRA_PAGES = [
    'https://texterra.ru/blog/author_vladimir-lakodin/',
    'https://texterra.ru/blog/author_vladimir-lakodin/?PAGEN_1=2',
    'https://texterra.ru/blog/author_vladimir-lakodin/?PAGEN_1=3',
    'https://texterra.ru/blog/author_aleksandr-khlynov/',
    'https://texterra.ru/blog/author_aleksandr-khlynov/?PAGEN_1=2',
    'https://texterra.ru/blog/author_milana-borisova/',
    'https://texterra.ru/blog/author_milana-borisova/?PAGEN_1=2',
    'https://texterra.ru/blog/author_milana-borisova/?PAGEN_1=3',
    'https://texterra.ru/blog/author_sergey-almakin/',
    'https://texterra.ru/blog/author_sergey-almakin/?PAGEN_1=2',
    'https://texterra.ru/blog/author_sergey-almakin/?PAGEN_1=3',
]

RUSSIADISCOVERY_PAGES = [
    'https://www.russiadiscovery.ru/news/tags/provereno_na_sebe/',
    'https://www.russiadiscovery.ru/news/tags/provereno_na_sebe/?page=2',
    'https://www.russiadiscovery.ru/news/tags/provereno_na_sebe/?page=3',
]

FREE_WRITER_PAGES = [
    'https://blog.vandrouki.ru/',
    'https://www.free-writer.ru/page/2',
    'https://www.free-writer.ru/page/3',
    'https://www.free-writer.ru/page/4',
    'https://www.free-writer.ru/page/5',
]

FREE_WRITER_PAGE = 'https://www.free-writer.ru/'

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
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/kinopoisk/{eng_title}')
    save_path.mkdir(parents=True, exist_ok=True)

    reviews = soup.find_all('span', {'class': '_reachbanner_'})
    for i, review in enumerate(reviews):
        review_text = review.get_text(' ', strip=True) # remove strip to get paragraphs
        filepath = save_path / Path(f'{i}.txt')
        with filepath.open('w', encoding='utf-8') as fout:
            fout.write(review_text)
        
        if TO_PRINT:
            print(review_text)


def parse_kinopoisk():
    for best_250_movies_page in KINOPOISK_BEST_250_MOVIES_PAGES: 
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{best_250_movies_page}'
        else:
            url_to_parse = best_250_movies_page
        
        resp = req.get(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        film_names = soup.find_all('a', {'class': 'selection-film-item-meta__link'}, href=True) # TODO: узнать про 250 ids фильмов, использовать неофициальную api
        for film_name in film_names:
            review_url = 'https://www.kinopoisk.ru' + film_name['href'] + 'reviews'
            print(review_url)
            parse_kinopoisk_film(review_url, to_save=TO_SAVE)

            time.sleep(60)


def parse_receipt(page_url: str, to_save: bool):
    if page_url[-1] != '/':
        page_url += '/'

    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
    
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    print(url_to_parse)
    
    header = soup.find_all('div', {'class': 'article-header'})[0]
    title = soup.find_all('h1')[0]
    
    title = title.get_text().replace(' ', '-')
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/receipts/povarenok')
    save_path.mkdir(parents=True, exist_ok=True)

    receipt_paragraphs = soup.find_all('div', {'class': 'cooking-bl'})
    receipt_text = ''
    for i, receipt_paragraph in enumerate(receipt_paragraphs):
        receipt_text += ' ' + receipt_paragraph.get_text(' ', strip=True) # remove strip to get paragraphs
    
    filepath = save_path / Path(f'{eng_title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(receipt_text)
    
    if TO_PRINT:
        print(receipt_text)


def parse_receipts():
    for povarenok_page in POVARENOK_RECEIPTS_PAGES:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{povarenok_page}'
        else:
            url_to_parse = povarenok_page

        resp = req.get(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        receipt_names = soup.find_all('div', {'class': 'm-img desktop-img conima'})
        for receipt_name in receipt_names:
            review_url = 'https://www.povarenok.ru/recipes/show/' + receipt_name['data-recipe']
            print(review_url)
            parse_receipt(review_url, to_save=TO_SAVE)
            # time.sleep(60)


def parse_politic_article_rbc(page_url: str, to_save: bool):
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
    
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    header = soup.find_all('h1', {'class': 'article__header__title-in js-slide-title'})[0]
    title = soup.find_all('h1')[0].get_text()

    if '. Видео' in title:
        return
    
    title = title.replace(' ', '-')
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/politics/rbc')
    save_path.mkdir(parents=True, exist_ok=True)

    article_body = soup.find_all('div', {'class': 'article__text article__text_free'})[0]
    article_text = article_body.get_text(' ', strip=True)
    
    filepath = save_path / Path(f'{eng_title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(article_text)
    
    if TO_PRINT:
        print(article_text)


def parse_politics():
    for rbc_politics_query_page in RBC_POLITICS_QUERY_PAGES:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{rbc_politics_query_page}'
        else:
            url_to_parse = rbc_politics_query_page

        print(url_to_parse)
        resp = req.get(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        politic_articles_names = soup.find_all('a', {'class': 'search-item__link'}, href=True)
        
        for i, politic_article in enumerate(politic_articles_names):
            print(politic_article['href'])
            parse_politic_article_rbc(politic_article['href'], to_save=TO_SAVE)
            time.sleep(1)

    if PARSE_FROM_RBC_POLITICS_MAIN:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{RBC_POLITICS_PAGE}'
        else:
            url_to_parse = RBC_POLITICS_PAGE
        resp = req.get(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        politic_articles_names = soup.find_all('a', {'class': 'item__link'}, href=True)
        for i, politic_article in enumerate(politic_articles_names):
            print(politic_article['href'])
            parse_politic_article_rbc(politic_article['href'], to_save=TO_SAVE)
            time.sleep(1)


def parse_wiki_how_article(page_url: str, to_save: bool, use_prefix: bool = True):
    if use_prefix:
        page_url = 'https://ru.wikihow.com' + page_url
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
    
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    headers = soup.find_all('h1', {'class': 'title_sm'})
    if len(headers) == 0:
        headers = soup.find_all('h1', {'class': 'title_md'})
        if len(headers) == 0:
            headers = soup.find_all('h1', {'class': 'title_lg'})
            if len(headers) == 0:
                return

    header = headers[0].get_text()
    
    title = header.replace(' ', '-')
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/wiki-how')
    save_path.mkdir(parents=True, exist_ok=True)

    article_section_0 = soup.find_all('div', {'class': 'mf-section-0'})[0]
    article_text = article_section_0.get_text(' ', strip=True)

    text_steps = soup.find_all('div', {'class': 'step'})

    for text_step in text_steps:
        article_text += ' ' + text_step.get_text(' ', strip=True)

    removal_list = [" X Источник информации", " Источник информации"]
    for phrase in removal_list:
        article_text = article_text.replace(phrase, "")
    
    filepath = save_path / Path(f'{eng_title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(article_text)
    
    if TO_PRINT:
        print(article_text)

        
def parse_wiki_how():
    for wiki_category_page in WIKI_HOW_CATEGORY_PAGES:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{wiki_category_page}'
        else:
            url_to_parse = wiki_category_page
        
        resp = req.get(url_to_parse)
        print(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        wikihow_articles_names = soup.find_all('div', {'class': 'responsive_thumb'})
        for i, wikihow_article in enumerate(wikihow_articles_names):
            if i > 10:
                continue
            wikihow_article_body = wikihow_article.find_all('a', href=True)[0]
            print(wikihow_article_body['href'])
            parse_wiki_how_article(wikihow_article_body['href'], to_save=TO_SAVE, use_prefix=False)
            time.sleep(1)

    if PARSE_FROM_WIKI_HOW_MAIN:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{WIKI_HOW_PAGE_MAIN}'
        else:
            url_to_parse = WIKI_HOW_PAGE_MAIN
        
        resp = req.get(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        wikihow_articles_names = soup.find_all('div', {'class': 'hp_thumb'})
        for i, wikihow_article in enumerate(wikihow_articles_names):
            wikihow_article_body = wikihow_article.find_all('a', href=True)[0]
            print(wikihow_article_body['href'])
            parse_wiki_how_article(wikihow_article_body['href'], to_save=TO_SAVE)
            time.sleep(1)


def parse_psychojournal_article(page_url: str, to_save: bool):
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
    
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    headers = soup.find_all('span', {'id': 'news-title'})
    header = headers[0].get_text()
    
    title = header.replace(' ', '-')
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/psychohournal')
    save_path.mkdir(parents=True, exist_ok=True)

    article_text = soup.find_all('div', {'class': 'mr underline'})[0]
    article_text = article_text.get_text(' ', strip=True)
    
    filepath = save_path / Path(f'{eng_title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(article_text)
    
    if TO_PRINT:
        print(article_text)

        
def parse_psychojournal():
    for psychojournal_page in PSYCHOJOURNAL_PAGES:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{psychojournal_page}'
        else:
            url_to_parse = psychojournal_page
        
        resp = req.get(url_to_parse)
        print(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        psychojournal_articles_names = soup.find_all('div', {'class': 'span6 mt'})
        for i, psychojournal_article in enumerate(psychojournal_articles_names):
            psychojournal_body = psychojournal_article.find_all('a', href=True)[0]
            print(psychojournal_body['href'])
            parse_psychojournal_article(psychojournal_body['href'], to_save=TO_SAVE)
            time.sleep(1)


def parse_texterra_article(page_url: str, to_save: bool):
    page_url = 'https://texterra.ru' + page_url
    print(page_url)
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
     
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    headers = soup.find_all('h1', {'class': 'article-head-block__title'})
    if len(headers) == 0:
        headers = soup.find_all('div', {'class': 'article-info-old__title'})
        print(headers)
        header = page_url.replace('https://texterra.ru/blog/', '').replace('.html', '')
    else:
        header = headers[0].get_text()
    
    title = header.replace(' ', '-')
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/texterra')
    save_path.mkdir(parents=True, exist_ok=True)

    article_text = soup.find_all('div', {'class': 'article-content'})[0]
    article_text = article_text.get_text(' ', strip=True)
    
    filepath = save_path / Path(f'{eng_title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(article_text)
    
    if TO_PRINT:
        print(article_text)

        
def parse_texterra():
    for psychojournal_page in TEXTERRA_PAGES:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{psychojournal_page}'
        else:
            url_to_parse = psychojournal_page
        
        resp = req.get(url_to_parse)
        print(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        texterra_articles_names = soup.find_all('a', {'class': 'article-card__title'}, href=True)
        for i, texterra_article in enumerate(texterra_articles_names):
            parse_texterra_article(texterra_article['href'], to_save=TO_SAVE)
            time.sleep(1)


def parse_russiadiscovery_article(page_url: str, to_save: bool):
    page_url = 'https://www.russiadiscovery.ru' + page_url
    print(page_url)
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
     
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    headers = soup.find_all('h1')
    print(headers)
    header = headers[0].get_text()
    title = header.replace(' ', '-')
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/russiadiscovery')
    save_path.mkdir(parents=True, exist_ok=True)

    article_text = soup.find_all('div', {'class': 'newsPage__content newsPage__content-with-offset'})[0]
    article_text = article_text.get_text(' ', strip=True)
    
    filepath = save_path / Path(f'{eng_title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(article_text)
    
    if TO_PRINT:
        print(article_text)

        
def parse_russiadiscovery():
    for discovery_page in RUSSIADISCOVERY_PAGES:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{discovery_page}'
        else:
            url_to_parse = discovery_page
        
        resp = req.get(url_to_parse)
        print(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        discovery_articles_names = soup.find_all('div', {'class': 'newsList__title'})
        for i, discovery_article in enumerate(discovery_articles_names):
            discovery_article_a = discovery_article.find_all('a', href=True)[0]
            parse_russiadiscovery_article(discovery_article_a['href'], to_save=TO_SAVE)
            time.sleep(1)


def parse_vandrouki_article(page_url: str, to_save: bool):
    print(page_url)
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
     
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    title = page_url.replace('https://blog.vandrouki.ru/', '')
    eng_title = translit(title, language_code='ru', reversed=True)

    save_path = ROOT_DIR / Path(f'data/vandrouki')
    save_path.mkdir(parents=True, exist_ok=True)

    article_texts = soup.find_all('div', {'class': 't030'})
    full_text = ''
    for article_text in article_texts:
        full_text += article_text.get_text(' ', strip=True)
    
    filepath = save_path / Path(f'{eng_title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(full_text)
    
    if TO_PRINT:
        print(full_text)


def parse_vandrouki():
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{VANDROUKI_PAGE}'
    else:
        url_to_parse = VANDROUKI_PAGE
    
    resp = req.get(url_to_parse)
    print(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    vandrouki_articles_names = soup.find_all('div', {'class': 't-item'})
    
    for i, vandrouki_article in enumerate(vandrouki_articles_names):
        vandrouki_article_a_list = vandrouki_article.find_all('a', href=True)
        if len(vandrouki_article_a_list) == 0:
            continue
        else:
            vandrouki_article_a = vandrouki_article_a_list[0]
        parse_vandrouki_article(vandrouki_article_a['href'], to_save=TO_SAVE)
        time.sleep(1)



def parse_free_writer_article(page_url: str, to_save: bool):
    print(page_url)
    if TO_USE_GOOGLE_CASH:
        url_to_parse = f'{GOOGLE_CASH_BASE}{page_url}'
    else:
        url_to_parse = page_url
     
    resp = req.get(url_to_parse)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    title = page_url.replace('https://www.free-writer.ru/pages/', '')
    title = title.replace('.html', '')

    save_path = ROOT_DIR / Path(f'data/free-writer')
    save_path.mkdir(parents=True, exist_ok=True)

    article_texts = soup.find_all('p')
    article_text = ''

    for text in article_texts:
        article_text += text.get_text(' ', strip=True)
    
    filepath = save_path / Path(f'{title}.txt')
    with filepath.open('w', encoding='utf-8') as fout:
        fout.write(article_text)
    
    if TO_PRINT:
        print(article_text)

        
def parse_free_writer():
    for free_writer_page in FREE_WRITER_PAGES:
        if TO_USE_GOOGLE_CASH:
            url_to_parse = f'{GOOGLE_CASH_BASE}{free_writer_page}'
        else:
            url_to_parse = free_writer_page
        
        resp = req.get(url_to_parse)
        print(url_to_parse)
        soup = BeautifulSoup(resp.text, 'lxml')
        free_writer_articles_names = soup.find_all('h2', {'class': 'entry-title'})
        for i, free_writer_article in enumerate(free_writer_articles_names):
            free_writer_article_a = free_writer_article.find_all('a', href=True)[0]
            parse_free_writer_article(free_writer_article_a['href'], to_save=TO_SAVE)
            time.sleep(1)


def main():
    """Main parsing method."""
    if TO_PARSE_KINOPOISK:
        parse_kinopoisk()
    if TO_PARSE_RECEIPTS:
        parse_receipts()
    if TO_PARSE_POLITICS:
        parse_politics()
    if TO_PARSE_WIKI_HOW:
        parse_wiki_how()
    if TO_PARSE_PSYCHOJOURNAL:
        parse_psychojournal()
    if TO_PARSE_TEXTERRA:
        parse_texterra()
    if TO_PARSE_RUSSIADISCOVERY:
        parse_russiadiscovery()
    if TO_PARSE_VANDROUKI:
        parse_vandrouki()
    if TO_PARSE_FREE_WRITER:
        parse_free_writer()


if __name__ == '__main__':
    main()
