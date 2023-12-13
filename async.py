import asyncio
import json
import time

import httpx
import requests
from bs4 import BeautifulSoup

HOME_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"

PRODUCT_URL = (
    "https://www.mcdonalds.com/dnaapp/item"
    "Details?country=UA&language=uk&showLiveData=true&item="
)


async def parse_single_product(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url)

    data = response.json()
    return dict(
        name=data["item"]["item_name"],
        description=data["item"]["description"],
        calories=data["item"]["nutrient_facts"]["nutrient"][2]["value"],
        fats=data["item"]["nutrient_facts"]["nutrient"][3]["value"],
        carbs=data["item"]["nutrient_facts"]["nutrient"][5]["value"],
        proteins=data["item"]["nutrient_facts"]["nutrient"][7]["value"],
        unsat_fats=data["item"]["nutrient_facts"]["nutrient"][4]["value"],
        sugar=data["item"]["nutrient_facts"]["nutrient"][6]["value"],
        salt=data["item"]["nutrient_facts"]["nutrient"][8]["value"],
        portion=data["item"]["nutrient_facts"]["nutrient"][0]["value"],
    )


async def get_all_products() -> None:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    product_soups = soup.select("li.cmp-category__item")

    product_ids = [
        product.get("data-product-id", None) for product in product_soups
    ]
    result = []
    async with httpx.AsyncClient() as client:
        for product in product_ids:
            url = PRODUCT_URL + product
            res = await parse_single_product(client, url)
            result.append(res)

    with open("async_data.json", "w", encoding="utf-8") as data_json:
        json.dump(result, data_json, ensure_ascii=False)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(get_all_products())
    end = time.perf_counter()

    print("Elapsed:", end - start)
