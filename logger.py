import logging
def get_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('logs.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger

logger = get_logger()