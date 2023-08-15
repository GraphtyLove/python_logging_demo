import random
import logging


db_logger = logging.getLogger("BOUMAN_DB")
db_logger.setLevel(logging.WARNING)

def add_to_db(article: str):
    data_is_added = random.choice([True, False])
    if data_is_added:
        db_logger.info("Article added to db!")
    else:
        db_logger.critical("Article failed to be added to DB!")