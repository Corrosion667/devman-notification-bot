"""This is a bot for checking devman lessons status."""

import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'
LONG_POLLING_TIMEOUT = 90
CONNECTION_LOST_TIMEOUT = 60
HTTP_ERROR_TIMEOUT = 100
HTTP_ERROR_NOTIFICATION = '{exception}\nError with Devman Api, retrying in {timeout} seconds.'

REVIEW_NOTIFICATION = 'Dear {user}! Your work «{title}» has been checked!\n{link}\n\n{result}'
POSITIVE_RESULT = 'Everything is great, you can get to the next lesson!'
NEGATIVE_RESULT = 'Unfortunately, some mistakes have been found in your task. Please try again.'

logger = logging.getLogger('devman_bot')
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s)')


class DevmanBot(object):
    """Class for devman notification bot."""

    def __init__(self, devman_token, telegram_token, telegram_chat_id, username):
        """Initiate bot instance.

        Args:
            devman_token: personal student token from *dvmn.org* to use its API.
            telegram_token: bot token from @BotFather in telegram.
            telegram_chat_id: id of a person from @userinfobot.
            username: the name with which the bot will address the userю
        """
        self.headers = {
            'Authorization': f'Token {devman_token}',
        }
        self.bot = telegram.Bot(token=telegram_token)
        self.telegram_chat_id = telegram_chat_id
        self.username = username
        self.url = LONG_POLLING_URL

    def start(self):
        """Start the bot."""
        self.bot.send_message(
            chat_id=self.telegram_chat_id,
            text=f'Hello, {self.username}!',
        )
        logger.info('Bot has started')
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
                response.raise_for_status()
            except ReadTimeout:
                logger.info('No new information from Api Devman received.')
                continue
            except ConnectionError:
                logger.warning(
                    f'Connection lost! Retrying in {CONNECTION_LOST_TIMEOUT} seconds.',
                )
                time.sleep(CONNECTION_LOST_TIMEOUT)
                continue
            except HTTPError as exc:
                error_message = HTTP_ERROR_NOTIFICATION.format(
                    exception=exc, timeout=HTTP_ERROR_TIMEOUT,
                )
                logger.error(error_message)
                self.bot.send_message(
                    chat_id=self.telegram_chat_id,
                    text=error_message,
                )
                time.sleep(HTTP_ERROR_TIMEOUT)
                continue
            reviews_data = response.json()
            if reviews_data.get('status') == 'timeout':
                request_time = reviews_data.get('timestamp_to_request')
                logger.info('No new information from Api Devman received.')
                continue
            request_time = reviews_data.get('last_attempt_timestamp')
            self.send_notification(reviews_data)

    def send_notification(self, reviews_data):
        """Send notification to user depending on Api Devman response with lessons reviews.

        Args:
            reviews_data: Api Devman information about lesson checking.
        """
        work_information = reviews_data.get('new_attempts')[0]
        is_work_failed = work_information.get('is_negative')
        lesson_title = work_information.get('lesson_title')
        lesson_url = work_information.get('lesson_url')
        notification = REVIEW_NOTIFICATION.format(
            user=self.username,
            title=lesson_title,
            link=lesson_url,
            result=NEGATIVE_RESULT if is_work_failed else POSITIVE_RESULT,
        )
        logger.info('New data about lesson checking found! Sending message.')
        self.bot.send_message(
            chat_id=self.telegram_chat_id,
            text=notification,
        )


def main():
    """Execute bot as a script."""
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    username = os.getenv('USERNAME', 'friend')
    bot = DevmanBot(
        devman_token,
        telegram_token,
        telegram_chat_id,
        username,
    )
    bot.start()


if __name__ == '__main__':
    main()
