from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementNotInteractableException,
)
import pandas
from webdriver_manager.chrome import ChromeDriverManager

from utils import read_config


def webdriver_start(mode="h") -> WebDriver:
    # headless mode
    if mode == "h":
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--lang=ja-JP")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
        )

        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    # normal mode
    if mode == "n":
        options = Options()
        # options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        )

        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )


def signin_rs(url, user_id, password):
    # driver = webdriver_start(mode="n")
    driver = webdriver_start()

    driver.get(url)
    driver.maximize_window()
    user_card_no = driver.find_element(by=By.ID, value="form-login-id")
    user_card_no.send_keys(user_id)
    user_password = driver.find_element(by=By.ID, value="form-login-pass")
    user_password.send_keys(password)
    signin_button = driver.find_element(by=By.ID, value="login-btn")
    signin_button.click()

    sleep(3)

    # hit 投資信託 button
    a_element = driver.find_element(
        by=By.XPATH, value='//a[span[contains(text(), "投資信託")]]'
    )
    a_element.click()

    # hit normal mode if it happens
    try:
        normal_mode_button = driver.find_element(
            by=By.CLASS_NAME, value="modal__button--normal"
        )
        normal_mode_button.click()
    except ElementNotInteractableException:
        pass

    # hit 保有商品一覧 button
    a_element = driver.find_element(by=By.XPATH, value='//a[img[@title="保有商品一覧"]]')
    a_element.click()

    table_element = driver.find_element(
        by=By.XPATH,
        value=f'//table[@id="poss-tbl-sp"]',
    )
    df_fund = pandas.read_html(table_element.get_attribute("outerHTML"))[0]
    values = [
        element.split("\t")[0]
        for element in df_fund.loc[:, "時価評価額 評価損益"].to_list()
        if element == element
    ]
    variations = [
        element.split("\t")[-1]
        for element in df_fund.loc[:, "時価評価額 評価損益"].to_list()
        if element == element
    ]
    df_show = df_fund.loc[list(range(0, 16, 3)), ["ファンド"]]
    df_show["時価評価額"] = values
    df_show["評価損益"] = variations
    return df_show


def get_prices():
    config = read_config("config.yaml")
    for key in config.keys():
        goods = config[key]
        text = signin_rs(goods["url"], goods["user_id"], goods["password"])
        break
    return text.to_markdown(index=False)


if __name__ == "__main__":
    pass
