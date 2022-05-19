import json
from app_service.app import redis_session

user_dict_name = 'users'
hotels_dict_name = 'hotels'
advertisers_dict_name = 'advertisers'
hotels_min_offers_dict_name = 'hotels_min_offers'

def get_users():
    users = redis_session.get_dict(user_dict_name)
    del users['_trick']
    for user, frequency in users.items():
        users[user] = int(frequency)

    return len(users), users


def get_hotels():
    hotels = redis_session.get_dict(hotels_dict_name)
    del hotels['_trick']
    for hotel, frequency in hotels.items():
        hotels[hotel] = int(frequency)

    return len(hotels), hotels

def get_advertisers():
    advertisers = redis_session.get_dict(advertisers_dict_name)
    del advertisers['_trick']
    for advertiser, frequency in advertisers.items():
        advertisers[advertiser] = int(frequency)

    return len(advertisers), advertisers

def get_hotel_per_advertiser_min_offer():
    results = []
    hotels_min_offers = redis_session.get_dict(hotels_min_offers_dict_name)
    del hotels_min_offers['_trick']
    for hotel, offers_per_advertiser in hotels_min_offers.items():
        hotels_min_offers[hotel] = json.loads(offers_per_advertiser)
        # for advertiser, min_offer in hotels_min_offers[hotel].items():
        #     results.append([hotel, advertiser, min_offer])
    return hotels_min_offers
