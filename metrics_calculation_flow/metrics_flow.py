import json
from utilities.logging_utility import logger
from metrics_calculation_flow.configs import *
from utilities.kafka_utility.consumer_util import Consumer
from utilities.redis_utility.redis_util import RedisUtility


class MetricsFlow:
    def __init__(self):
        self.data_consumer = Consumer()
        self.rds = RedisUtility()

    def init_redis_dicts(self):
        for dict_name in REDIS_DICT_NAMES:
            if self.rds.get_dict(dict_name):
                logger.info(msg=f'Redis dict {dict_name} exists')
                continue
            else:
                self.rds.init_empty_dict(dict_name)
                logger.info(msg=f'Redis dict {dict_name} created')

    def get_data(self):
        for message in self.data_consumer.consume(KAFKA_INPUT_TOPICS):
            yield message

    def update_metrics_dicts(self, data_obj):
        def update_users(user_id):
            if self.rds.is_dict_key_exist(USERS_DICT_NAME, user_id):
                value = int(self.rds.get_from_dict(USERS_DICT_NAME, user_id))
                self.rds.insert_to_dict(USERS_DICT_NAME, user_id, value + 1)
            else:
                self.rds.insert_to_dict(USERS_DICT_NAME, user_id, 1)

        def update_hotels(hotel_id):
            if self.rds.is_dict_key_exist(HOTELS_DICT_NAME, hotel_id):
                value = int(self.rds.get_from_dict(HOTELS_DICT_NAME, hotel_id))
                self.rds.insert_to_dict(HOTELS_DICT_NAME, hotel_id, value + 1)
            else:
                self.rds.insert_to_dict(HOTELS_DICT_NAME, hotel_id, 1)

        def update_advertisers(advertisers):
            for advertiser in advertisers:
                if self.rds.is_dict_key_exist(ADVERTISERS_DICT_NAME, advertiser):
                    value = int(self.rds.get_from_dict(ADVERTISERS_DICT_NAME, advertiser))
                    self.rds.insert_to_dict(ADVERTISERS_DICT_NAME, advertiser, value + 1)
                else:
                    self.rds.insert_to_dict(ADVERTISERS_DICT_NAME, advertiser, 1)

        def update_hotels_min_offers(hotel_id, min_offer):
            if self.rds.is_dict_key_exist(HOTELS_MIN_OFFER_DICT_NAME, hotel_id):
                # Get the hotel current advertisers with min offer prices
                value = json.loads(self.rds.get_from_dict(HOTELS_MIN_OFFER_DICT_NAME, hotel_id))
                # Get current advertiser min offer price
                curr_advertiser_price = value.get(min_offer['advertiser'], 1e18)
                # Update the advertiser current minimum offer price with respect to new offer price
                value[min_offer['advertiser']] = min(curr_advertiser_price, min_offer['price'])
                self.rds.insert_to_dict(HOTELS_MIN_OFFER_DICT_NAME, hotel_id, json.dumps(value))
            else:
                # Create new hotel and init it's advertisers list
                self.rds.insert_to_dict(
                    HOTELS_MIN_OFFER_DICT_NAME,
                    hotel_id,
                    json.dumps({
                        min_offer['advertiser']: min_offer['price']
                    })
                )

        update_users(data_obj['user_id'])
        update_hotels(data_obj['hotel_id'])
        update_advertisers(data_obj['advertisers'])
        update_hotels_min_offers(data_obj['hotel_id'], data_obj['min_offer'])

    def run(self):
        self.init_redis_dicts()
        data = self.get_data()
        for message in data:
            self.update_metrics_dicts(message)
