import logging
import os
from datetime import datetime

def get_logger(logger_name):
    # create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # create a log file name based on the current date and time
    log_file = datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log")

    # create a file handler for the log file
    file_handler = logging.FileHandler(os.path.join(logs_dir, log_file))

    # set the format of the log messages
    # formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s - %(lineno)d")

    file_handler.setFormatter(formatter)

    # create a logger object and add the file handler to it
    logger = logging.getLogger(logger_name)
    logger.addHandler(file_handler)
    
    logger.setLevel(logging.INFO)


    return logger
