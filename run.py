from communication import send_message, run_image
from crawler import get_prices, get_todays_news
from utils import read_config

prices = get_prices()
text = get_todays_news()

user_ids = read_config("line.yaml")["USER_ID"]
for user_id in user_ids:
    run_image(user_id)
    send_message(text, user_id)
