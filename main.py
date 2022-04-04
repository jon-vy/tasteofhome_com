import re
import time
import requests
from bs4 import BeautifulSoup
import lxml
from user_agent import generate_user_agent
import asyncio
import aiohttp
import json
from random import randint
from proxy import login, password, ip, port


total_list = []
proxies = {'https': f'http://{login}:{password}@{ip}:{port}'}
def get_url():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
    url = "https://www.tasteofhome.com/collection/clean-eating-recipes/"
    links_list = []
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        pass
    elif r.status_code == 403:
        r = requests.get(url=url, headers=headers, proxies=proxies)
        if r.status_code == 200:
            pass
    html_cod = r.text
    soup = BeautifulSoup(html_cod, "lxml")
    urls = soup.find_all('h2', class_='listicle-page__title')
    for url in urls:
        link = url.find('a').get('href')
        links_list.append(link)
    return links_list


async def pars_date(session, url):
    proxy = f'http://{login}:{password}@{ip}:{port}'
    try:
        await asyncio.sleep(randint(1, 5))
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "User-Agent": generate_user_agent()
        }
        async with session.get(url=url, headers=headers, proxy=proxy) as r:

            if r.status == 200:
                pass
            elif r.status == 403:
                async with session.get(url=url, headers=headers, proxy=proxy) as r:
                    if r.status == 200:
                        pass

            html_cod = await r.text()
            soup = BeautifulSoup(html_cod, "lxml")
            name = soup.find("h1", class_="recipe-title").text
            description = soup.find("div", class_="recipe-tagline__text").text.strip()
            total_time = soup.find("div", class_="total-time").find("p").text.strip()
            makes = soup.find("div", class_="makes").find("p").text

            try:
                photo = soup.find("div", class_="featured-container").find_all("img")[2].get("data-lazy-src").split('?')[0]
            except:
                photo = soup.find("meta", property="og:image").get("content")

            ingredients_list = []
            ingredients = soup.find("div", class_="recipe-ingredients").find_all("li")
            for ingredient in ingredients:
                ingredients_list.append(ingredient.text.strip())

            directions_list = []
            directions = soup.find("ol", class_="recipe-directions__list").find_all("li")
            for direction in directions:
                directions_list.append(direction.text.strip())

            tips_list = []
            try:
                tips = soup.find("div", class_="recipe-editors-note").find_all("li")
                for tip in tips:
                    tips_list.append(tip.text.strip())
            except:
                tips_list.append("no informations")

            nutrition_facts = soup.find("div", class_="recipe-nutrition-facts").find("p").text.strip()

            total_list.append(
                {
                    "name": name,
                    "photo": photo,
                    "link": url,
                    "Total_Time": total_time,
                    "servings": makes,
                    "ingredients": ingredients_list,
                    "description": description,
                    "directions": directions_list,
                    "nutrients": nutrition_facts,
                    "tips": tips_list
                }
            )
        print(f"Обработал {url}")
    except:
        print(f"ошибка {url}")



async def gahter_date():
    async with aiohttp.ClientSession() as session:
        links_list = get_url()
        tasks = []  # список задач
        for link in links_list:  #[1:3]
            task = asyncio.create_task(pars_date(session, link))  # создал задачу
            tasks.append(task)  # добавил её в список
        await asyncio.gather(*tasks)


def main():
    asyncio.get_event_loop().run_until_complete(gahter_date())
    with open("tasteofhome.json", "w") as f:
        json.dump(total_list, f)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Время работы {total_time}")

