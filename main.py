import json
import requests
from selenium import webdriver
from get_prod_info import get_prod_info


product = "шапка"
limit = 10


options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

search_url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=mmr_21&TestID=388&appType=1&curr=rub&dest=-1257786&resultset=catalog&sort=popular&spp=27&suppressSpellcheck=false&query={product}"
search_url_by_asc = (
    "https://wildberries.ru/catalog/0/search.aspx?page=1&sort=priceup&search=" + product
)

req = requests.get(search_url)
raw_products = json.loads(req.text)["data"]["products"][::limit]

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
