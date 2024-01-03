import json
import requests
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_prod_info(prod_id, browser):
    url = f"https://www.wildberries.ru/catalog/{prod_id}/detail.aspx"
    classname = "photo-zoom__preview.j-zoom-image.hide"

    browser.get(url)
    sleep(1)
    browser.find_element(By.TAG_NAME, "html").send_keys(Keys.END)
    sleep(1)
    feedbacks = get_feedbacks(browser)
    img = browser.find_element(By.CLASS_NAME, classname)
    card_href = img.get_attribute("src")
    start_index = card_href.index("images/")

    url = (card_href[:start_index]) + "info/ru/card.json"

    data = json.loads(requests.get(url).text)
    meta_tags = browser.find_elements(By.TAG_NAME, "meta")
    metas = []
    for meta_tag in meta_tags:
        meta = dict()
        name = meta_tag.get_attribute("name")
        content = meta_tag.get_attribute("content")
        if not name or not content:
            continue
        meta["name"] = name
        meta["content"] = content

        metas.append(meta)

    return data["description"], feedbacks, meta


def get_feedbacks(browser):
    classname = "swiper-slide.comment-card.j-feedback-slide"
    feedbacks_divs = browser.find_elements(By.CLASS_NAME, classname)
    feedbacks = []

    for div in feedbacks_divs:
        feedback = dict()

        text = div.find_element(
            By.CLASS_NAME, "comment-card__message.j-feedback-text"
        ).get_attribute("innerText")

        date = div.find_element(By.CLASS_NAME, "comment-card__date").get_attribute(
            "innerText"
        )

        stars: str = div.find_element(
            By.CLASS_NAME, "comment-card__stars.stars-line"
        ).get_attribute("class")

        start_index = stars.rindex("star")
        rank = stars[start_index + 4 :]

        feedback["text"] = text
        feedback["rank"] = rank
        feedback["date"] = date

        feedbacks.append(feedback)
    return feedbacks
