import logging

def setup_custom_logger():
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(module)s:  %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('app.log', mode='w')
    file_handler.setFormatter(formatter)

    # it captures the internal logs of Flask
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_custom_logger()