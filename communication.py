from linebot.exceptions import LineBotApiError
from linebot.v3.messaging import (
    MessagingApi,
    ApiClient,
    Configuration,
    TextMessage,
    PushMessageRequest,
)
from utils import read_config


CHANNEL_ACCESS_TOKEN = read_config("line.yaml")["CHANNEL_ACCESS_TOKEN"]
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)


def send_message(text, user_id):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        try:
            line_bot_api.push_message(
                PushMessageRequest(messages=[TextMessage(text=text)], to=user_id)
            )
        except LineBotApiError as e:
            print(e.message)


if __name__ == "__main__":
    text = "テストメッセージ"  # 好きな文章でOKです
    send_message(text)
