import json
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

HOME_URL = "https://www.mcdonalds.com/"

MENU_URL = urljoin(HOME_URL, "ua/uk-ua/eat/fullmenu.html")


def parse_single_product(driver, link: str) -> dict:
    second_row = 0
    while not second_row:
        driver.get(link)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        first_row = soup.select("li.cmp-nutrition-summary__heading-primary-item")
        second_row = soup.select(
            ".cmp-nutrition-summary__details-column-view-desktop li.label-item"
        )
    return dict(
        name=soup.select_one(".cmp-product-details-main__heading-title").text,
        description=soup.select_one(".cmp-text").text.strip(),
        calories=" ".join(
            first_row[0].select_one("span.sr-only.sr-only-pd").text.split()
        ),
        fats=" ".join(
            first_row[1].select_one("span.sr-only.sr-only-pd").text.split()
        ),
        carbs=" ".join(
            first_row[2].select_one("span.sr-only.sr-only-pd").text.split()
        ),
        proteins=" ".join(
            first_row[3].select_one("span.sr-only.sr-only-pd").text.split()
        ),
        unsat_fats=" ".join(
            second_row[0]
            .select_one("span.sr-only")
            .text.replace("Percent", "%")
            .split()
        ),
        sugar=" ".join(
            second_row[1]
            .select_one("span.sr-only")
            .text.replace("Percent", "%")
            .split()
        ),
        salt=" ".join(
            second_row[2]
            .select_one("span.sr-only")
            .text.replace("Percent", "%")
            .split()
        ),
        portion=second_row[3]
        .select_one("span.sr-only")
        .text.strip()
        .split()[0],
    )


def get_all_products() -> None:
    driver = webdriver.Chrome()

    page = requests.get(MENU_URL).content
    soup = BeautifulSoup(page, "html.parser")

    products_links = soup.select(".cmp-category__item-link")

    result = []

    for link in products_links:
        product = parse_single_product(
            driver, urljoin(HOME_URL, link["href"])
        )

        result.append(product)

    with open("data.json", "w", encoding="utf-8") as data_json:
        json.dump(result, data_json, ensure_ascii=False)

    driver.close()


if __name__ == "__main__":
    start = time.perf_counter()
    get_all_products()
    end = time.perf_counter()

    print("Elapsed:", end - start)
