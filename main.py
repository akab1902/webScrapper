from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

DRIVE_PATH = str(Path('chromedriver').resolve())
browser = webdriver.Chrome(executable_path=DRIVE_PATH)

def get_html(url):
    browser.get(url)
    return browser.page_source

def press_seemore():
    browser.find_element_by_css_selector('button.c-link--btn').click()

def scrap_data(article):
    try:
        a = article.find('a', class_ = "m-object__title__link")
    except:
        title = ''
        link = ''
    else:
        title = a.get('title')
        link = a.get('href')

    try:
        article_page = get_html("https://www.euronews.com"+link)
    except:
        content = ''
    else:
        article_soup = BeautifulSoup(article_page, 'lxml')
        content = article_soup.find_all('p')

    data = {'title': title, 'url': "https://www.euronews.com"+link, 'content': content}
    return data

def write_csv(articles):
    with open('results.csv', 'a') as f:
        fields = ['title', 'url', 'content']
        writer = csv.DictWriter(f, fieldnames=fields)
        for a in articles:
            writer.writerow(a)

def main(): 
    url = 'https://www.euronews.com/green/eco-innovation'
    html = get_html(url)
    time.sleep(5) # Let the user actually see something!
    soup = BeautifulSoup(html, 'lxml')

    # press_seemore()
    articles = soup.find_all(['h3', 'h2'], {'class' : "qa-article-title"})
    print(len(articles))

    articles_data = []
    for article in articles:
        data = scrap_data(article)
        articles_data.append(data)

    write_csv(articles_data)

    browser.quit()
    
if __name__ == '__main__':
    main()