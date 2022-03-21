"""This is a bot for checking devman lessons status."""

import os
import time

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, ReadTimeout

load_dotenv()

DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
USERNAME = os.getenv('USERNAME', 'friend')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'
LONG_POLLING_TIMEOUT = 90

NOTIFICATION = 'Dear {user}! Your work «{title}» has been checked!\n{link}\n\n{result}'
POSITIVE_RESULT = 'Everything is great, you can get to the next lesson!'
NEGATIVE_RESULT = 'Unfortunately, some mistakes have been found in your task. Please try again.'


class DevmanBot(object):
    """Class for devman notification bot."""

    def __init__(self):
        """Initiate bot instance."""
        self.headers = {
            'Authorization': f'Token {DEVMAN_TOKEN}',
        }
        self.bot = telegram.Bot(token=TELEGRAM_TOKEN)
        self.url = LONG_POLLING_URL

    def start(self):
        """Start the bot."""
        self.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f'Hello, {USERNAME}!',
        )
        request_time = str(time.time())
        while True:
            timestamp_data = {'timestamp': request_time}
            try:
                response = requests.get(
                    self.url,
                    timeout=LONG_POLLING_TIMEOUT,
                    headers=self.headers,
                    params=timestamp_data,
                ).json()
            except (ConnectionError, ReadTimeout):
                continue
            if response.get('status') == 'timeout':
                request_time = response.get('timestamp_to_request')
                continue
            request_time = response.get('last_attempt_timestamp')
            self.send_notification(response)

    def send_notification(self, response):
        """Send notification to user depending on Api Devman response.

        Args:
            response: Api Devman information about lesson checking.
        """
        work_information = response.get('new_attempts')[0]
        is_work_failed = work_information.get('is_negative')
        lesson_title = work_information.get('lesson_title')
        lesson_url = work_information.get('lesson_url')
        notification = NOTIFICATION.format(
            user=USERNAME,
            title=lesson_title,
            link=lesson_url,
            result=NEGATIVE_RESULT if is_work_failed else POSITIVE_RESULT,
        )
        self.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=notification,
        )


if __name__ == '__main__':
    bot = DevmanBot()
    bot.start()
