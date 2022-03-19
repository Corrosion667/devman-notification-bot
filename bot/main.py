"""This is a bot for checking devman lessons status."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')
LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'


class DevmanBot(object):
    """Class for devman notification bot."""

    def __init__(self):
        """Initiate bot instance with url for requests and auth dvman token."""
        self.headers = {
            'Authorization': f'Token {DEVMAN_TOKEN}',
        }
        self.url = LONG_POLLING_URL

    def start(self):
        """Start the bot."""
        while True:
            response = requests.get(
                self.url,
                headers=self.headers,
            )
            print(response.json())


if __name__ == '__main__':
    bot = DevmanBot()
    bot.start()
