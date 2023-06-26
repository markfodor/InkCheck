import logging

def setup_custom_logger():
    formatter = logging.Formatter(fmt = '%(asctime)s %(levelname)s %(module)s:  %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('inkcheck')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

logger = setup_custom_logger()