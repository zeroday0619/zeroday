import os
import logging
import functools
from rich.logging import RichHandler


class Logger:
    @staticmethod
    def generate_log():
        """
        Create a logger object

        :return: Logger object.
        """
        log_format = '%(levelname)s %(asctime)s %(message)s'

        # Create a logger and set the level.
        for i in ["bot", "ffmpeg", "youtube_dl", "asyncio", "subprocess"]:
            logger = logging.getLogger(i)
        logger.setLevel(logging.DEBUG)
        logger.handlers = [RichHandler(rich_tracebacks=True, show_time=True)]

        log_dir = os.path.expanduser("~/log")
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)

        # Create file handler, log format and add the format to file handler
        LOG_PATH = os.path.expanduser("~/log/zeroday.log")
        file_handler = logging.FileHandler(filename=LOG_PATH)

        # See https://docs.python.org/3/library/logging.html#logrecord-attributes
        # for log format attributes.

        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    @classmethod
    def set(cls):
        """
        We create a parent function to take arguments
        :return: log
        """
        def error_log(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                logger = cls.generate_log()
                try:
                    # Execute the called function, in this case `divide()`.
                    # If it throws an error `Exception` will be called.
                    # Otherwise it will be execute successfully.
                    if kwargs != {}:
                        logger.debug(kwargs)

                    result = func(*args, **kwargs)

                    if result is not None:
                        logger.debug(result)

                    return result
                except Exception as e:
                    error_msg = f"{e}"
                    logger.exception(msg=error_msg, exc_info=True)
                    return e  # Or whatever message you want.
            return wrapper
        return error_log
