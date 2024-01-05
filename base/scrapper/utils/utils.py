import json
import requests
from selenium import webdriver
from .get_prod_info import get_prod_info


def scrap_items(query, limit, sort_type):
    print(query, limit, sort_type)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    search_url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=mmr_21&TestID=388&appType=1&curr=rub&dest=-1257786&resultset=catalog&sort={sort_type}&spp=27&suppressSpellcheck=false&query={query}"
    req = requests.get(search_url)
    raw_products = json.loads(req.text)["data"]["products"][:limit]

    products = []
    for raw_prod in raw_products:
        prod = {
            "id": raw_prod["id"],
            "title": raw_prod["name"],
            "rate": raw_prod["reviewRating"],
            "feedbacks_count": raw_prod["feedbacks"],
            "price": str(raw_prod["priceU"])[:-2],
            "sale_price": str(raw_prod["salePriceU"])[:-2],
        }
        products.append(prod)
        prod["description"], prod["feedbacks"], prod["metas"] = get_prod_info(
            prod["id"],
            driver,
        )
    return products
