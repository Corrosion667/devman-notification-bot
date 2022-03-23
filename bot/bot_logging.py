"""Module for logging adjustment of the project."""

import logging

logger = logging.getLogger('devman_notification_bot')


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


def prepare_log_handlers(telegram_bot, telegram_chat_id):
    """Create two handlers: general and telegram handler for errors only.

    Args:
        telegram_bot: instance of telegram bot.
        telegram_chat_id: id of a person from @userinfobot.
    """
    log_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s',
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(log_formatter)
    tg_logs_handler = TelegramLogsHandler(telegram_bot, telegram_chat_id)
    tg_logs_handler.setLevel(logging.ERROR)
    tg_logs_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(tg_logs_handler)
