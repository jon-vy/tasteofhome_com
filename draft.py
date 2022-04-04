import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re
import lxml
total_list = []
url = "https://www.tasteofhome.com/recipes/pan-roasted-chicken-and-vegetables/"
# url = "https://www.tasteofhome.com/recipes/calico-scrambled-eggs/"
# url = "https://www.tasteofhome.com/recipes/loaded-quinoa-breakfast-bowl/"
def pars_date(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
    proxies = {'https': 'http://xhk3po:5CuNaq@45.153.20.219:13422'}
    r = requests.get(url=url, headers=headers, proxies=proxies)  # , auth=auth
    html_cod = r.text
    soup = BeautifulSoup(html_cod, 'lxml')

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
    print(photo)

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

if __name__ == '__main__':
    pars_date(url)