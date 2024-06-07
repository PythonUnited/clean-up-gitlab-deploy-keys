import os

from dotenv import load_dotenv
import gitlab


def get_gitlab_connection():
    load_dotenv()

    url = os.getenv("GITLAB_URL")
    token = os.getenv("ACCESS_TOKEN")

    if not url or not token:
        raise ValueError("GITLAB_URL and ACCESS_TOKEN must be set")

    return gitlab.Gitlab(url, private_token=token)
