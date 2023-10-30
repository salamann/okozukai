from ftplib import FTP_TLS
import hashlib

from linebot.exceptions import LineBotApiError
from linebot.v3.messaging import (
    MessagingApi,
    ApiClient,
    Configuration,
    TextMessage,
    ImageMessage,
    PushMessageRequest,
)
from utils import read_config


CHANNEL_ACCESS_TOKEN = read_config("line.yaml")["CHANNEL_ACCESS_TOKEN"]
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

server_settings = read_config("server.yaml")


def send_message(text, user_id):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        try:
            line_bot_api.push_message(
                PushMessageRequest(messages=[TextMessage(text=text)], to=user_id)
            )
        except LineBotApiError as e:
            print(e.message)


def send_image(image_url, user_id):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        try:
            line_bot_api.push_message(
                PushMessageRequest(
                    messages=[
                        ImageMessage(
                            originalContentUrl=image_url,
                            previewImageUrl=image_url,
                        )
                    ],
                    to=user_id,
                )
            )
        except LineBotApiError as e:
            print(e.message)


def upload_image(
    host_name: str, user_name: str, password: str, local_path: str, remote_path: str
) -> None:
    with FTP_TLS(host=host_name, user=user_name, passwd=password) as ftp:
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}", f)


def remove_image(
    host_name: str, user_name: str, password: str, remote_path: str
) -> None:
    with FTP_TLS(host=host_name, user=user_name, passwd=password) as ftp:
        ftp.delete(remote_path)


def run_image(user_id):
    local_name = "table_plotly.png"
    sha_name = create_sha(local_name) + ".png"
    remote_path = server_settings["remote_path"] + sha_name
    image_url = server_settings["image_url"] + sha_name
    upload_image(
        server_settings["host_name"],
        server_settings["user_name"],
        server_settings["password"],
        local_name,
        remote_path,
    )
    send_image(image_url, user_id)


def create_sha(image_file):
    with open(image_file, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    return sha256


if __name__ == "__main__":
    pass
