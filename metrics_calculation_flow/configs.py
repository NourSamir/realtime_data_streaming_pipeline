# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

USERS_DICT_NAME = os.getenv('REDIS_USERS_DICT_NAME', 'users')

HOTELS_DICT_NAME = os.getenv('REDIS_HOTELS_DICT_NAME', 'hotels')

ADVERTISERS_DICT_NAME = os.getenv('REDIS_ADVERTISERS_DICT_NAME', 'advertisers')

HOTELS_MIN_OFFER_DICT_NAME = os.getenv('REDIS_HOTELS_MIN_OFFER_DICT_NAME', 'hotels_min_offers')

REDIS_DICT_NAMES = [
    USERS_DICT_NAME,
    HOTELS_DICT_NAME,
    ADVERTISERS_DICT_NAME,
    HOTELS_MIN_OFFER_DICT_NAME
]

KAFKA_INPUT_TOPICS = [os.getenv('KAFKA_PROCESSED_DATA_TOPIC', 'processed_events')]
