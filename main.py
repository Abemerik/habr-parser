import requests
from bs4 import BeautifulSoup
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

url = "https://habr.com/ru/articles/top/daily/"

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9'
            }

def parser_title():
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        articles_data = []
        articles = soup.find_all("article", class_="tm-articles-list__item")
        for article in articles:
            title = article.find("a", class_="tm-title__link")
            views = article.find("span", class_="tm-icon-counter__value")
            if title and views:
                articles_data.append((title.text.strip(), views.text.strip()))

        with open("title.txt", "w", encoding="utf-8") as w:
            for title, views in articles_data:
                print(f"Title: {title.text} | Views: {views.text} \n")
                w.write(f"Title: {title.text} | Views: {views.text} \n")
        return "Парсинг успешно завершен"
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"
    except Exception as e:
        return f"Ошибка парсинга: {e}"

result = parser_title()
print(result)
