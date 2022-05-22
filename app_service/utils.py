# -*- coding: utf-8 -*-

import os
import json
from dotenv import load_dotenv
from app_service.app import redis_session

load_dotenv()


def get_users():
    user_dict_name = os.getenv('REDIS_USERS_DICT_NAME', 'users')
    users = redis_session.get_dict(user_dict_name)
    for user, frequency in users.items():
        users[user] = int(frequency)

    return len(users), users


def get_hotels():
    hotels_dict_name = os.getenv('REDIS_HOTELS_DICT_NAME', 'hotels')
    hotels = redis_session.get_dict(hotels_dict_name)
    for hotel, frequency in hotels.items():
        hotels[hotel] = int(frequency)

    return len(hotels), hotels

def get_advertisers():
    advertisers_dict_name = os.getenv('REDIS_ADVERTISERS_DICT_NAME', 'advertisers')
    advertisers = redis_session.get_dict(advertisers_dict_name)
    for advertiser, frequency in advertisers.items():
        advertisers[advertiser] = int(frequency)

    return len(advertisers), advertisers

def get_hotel_per_advertiser_min_offer():
    hotels_min_offers_dict_name = os.getenv('REDIS_HOTELS_MIN_OFFER_DICT_NAME', 'hotels_min_offers')

    results = []
    hotels_min_offers = redis_session.get_dict(hotels_min_offers_dict_name)
    for hotel, offers_per_advertiser in hotels_min_offers.items():
        hotels_min_offers[hotel] = json.loads(offers_per_advertiser)
        # for advertiser, min_offer in hotels_min_offers[hotel].items():
        #     results.append([hotel, advertiser, min_offer])
    return hotels_min_offers

