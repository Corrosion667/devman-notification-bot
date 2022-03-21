"""This is a bot for checking devman lessons status."""

import os
import time

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout

load_dotenv()

DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
USERNAME = os.getenv('USERNAME', 'friend')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'
LONG_POLLING_TIMEOUT = 90
CONNECTION_LOST_TIMEOUT = 60
HTTP_ERROR_TIMEOUT = 100
HTTP_ERROR_NOTIFICATION = '{exception}\nError with Devman Api, retrying in {timeout} seconds.'

REVIEW_NOTIFICATION = 'Dear {user}! Your work «{title}» has been checked!\n{link}\n\n{result}'
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
        request_time = time.time()
        while True:
            timestamp_data = {'timestamp': request_time}
            try:
                response = requests.get(
                    self.url,
                    timeout=LONG_POLLING_TIMEOUT,
                    headers=self.headers,
                    params=timestamp_data,
                )
            except ReadTimeout:
                continue
            except ConnectionError:
                time.sleep(CONNECTION_LOST_TIMEOUT)
                continue
            try:
                response.raise_for_status()
            except HTTPError as exc:
                self.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=HTTP_ERROR_NOTIFICATION.format(exception=exc, timeout=HTTP_ERROR_TIMEOUT),
                )
                time.sleep(HTTP_ERROR_TIMEOUT)
                continue
            decoded_response = response.json()
            if decoded_response.get('status') == 'timeout':
                request_time = decoded_response.get('timestamp_to_request')
                continue
            request_time = decoded_response.get('last_attempt_timestamp')
            self.send_notification(decoded_response)

    def send_notification(self, response):
        """Send notification to user depending on Api Devman response.

        Args:
            response: Api Devman information about lesson checking.
        """
        work_information = response.get('new_attempts')[0]
        is_work_failed = work_information.get('is_negative')
        lesson_title = work_information.get('lesson_title')
        lesson_url = work_information.get('lesson_url')
        notification = REVIEW_NOTIFICATION.format(
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
