import random

def add_to_db(article: str):
    data_is_added = random.choice([True, False])
    if data_is_added:
        print("Article added to db!")
    else:
        print("Article failed to be added to DB!")