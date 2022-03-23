"""Module with logs handler to send them to telegram."""

import logging


class TelegramLogsHandler(logging.Handler):
    """Class for handler of logs to send them to TG."""

    def __init__(self, tg_bot, telegram_chat_id):
        """Initiate handler instance.

        Args:
            tg_bot: instance of telegram bot.
            telegram_chat_id: id of a person from @userinfobot.
        """
        super().__init__()
        self.tg_bot = tg_bot
        self.telegram_chat_id = telegram_chat_id

    def emit(self, record):
        """Send log record to telegram chat.

        Args:
            record: text log to be sent.
        """
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.telegram_chat_id, text=log_entry)
