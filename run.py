from communication import send_message
from crawler import get_prices
from utils import read_config

prices = get_prices()

user_ids = read_config("line.yaml")["USER_ID"]
for user_id in user_ids:
    send_message(prices, user_id)
