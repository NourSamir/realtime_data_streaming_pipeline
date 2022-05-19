import json
from utilities.logging_utility import logger
from metrics_calculation_flow.configs import *
from utilities.kafka_utility.consumer_util import Consumer
from utilities.redis_utility.redis_util import RedisUtility


class MetricsFlow:
    """
        MetricsFlow class to consume data messages from input_data_topics, calculate metrics over
        the consumed messages and load the updates to redis dictionaries.
        Attributes:
            data_consumer(Consumer): A kafka consumer object
            rds(RedisUtility): A redis utility object
    """
    def __init__(self):
        logger.info(msg='[MetricFlow.__init__]: Init the consumer and redis utility objects')
        """
            Summary:
                The MetricsFlow class constructor
            Description:
                Init a kafka consumer and redis utility
            Parameters:
        """
        self.data_consumer = Consumer()
        self.rds = RedisUtility()

    def init_redis_dicts(self):
        """
            Summary:
                Init N empty redis dictionaries
            Description:
                Init 4 empty redis dictionaries (users, hotels, advertisers, hotels_min_offers) if these 
                dictionaries have been created before then skip.
            Parameters:
            Returns:
        """
        logger.info(msg=f'[MetricsFlow.init_redis_dicts]: Start init redis dictionaries')
        for dict_name in REDIS_DICT_NAMES:
            if self.rds.get_dict(dict_name):
                logger.info(msg=f'[MetricsFlow.init_redis_dicts]: Redis dict {dict_name} exists')
                continue
            else:
                self.rds.init_empty_dict(dict_name)
                logger.info(msg=f'[MetricsFlow.init_redis_dicts]: Redis dict {dict_name} created')

    def get_data(self):
        """
            Summary:
                Run a kafka consumer
            Description:
                Init a kafka consumer that subscribes to processed_events topic
            Parameters:
            Returns:
        """
        logger.info(msg=f'[MetricsFlow.get_data]: A kafka consumer subscribes to {KAFKA_INPUT_TOPICS} has been started')
        for message in self.data_consumer.consume(KAFKA_INPUT_TOPICS):
            yield message

    def update_metrics_dicts(self, data_obj):
        """
            Summary:
                Update redis dictionaries values
            Description:
                Update redis dictionaries values with respect to the new data_obj calculated values,
                execute the update flow.
            Parameters:
                data_obj(dict): A python dictionary represents a data object as following
                {
                    "user_id": "21aee52a-a93e-496c-a368-eff34ce53736",
                    "hotel_id": "6036",
                    "search_timestamp": 1652913298.83403,
                    "advertisers": [
                        "Mercure",
                        "booking.com",
                    ],
                    "min_offer": {
                        "price": 12552,
                        "advertiser": "booking.com"
                    }
                }
            Returns:
        """

        def update_users(user_id):
            """
                Summary:
                    Update redis users dictionary
                Description:
                    Adjust the user frequency, Check if the user exists then add 1 to the current frequency value
                    or create a new user with frequency value = 1 if the user isn't exist
                Parameters:
                    user_id(str): User ID string
                Returns:
            """
            if self.rds.is_dict_key_exist(USERS_DICT_NAME, user_id):
                value = int(self.rds.get_from_dict(USERS_DICT_NAME, user_id))
                self.rds.insert_to_dict(USERS_DICT_NAME, user_id, value + 1)
            else:
                self.rds.insert_to_dict(USERS_DICT_NAME, user_id, 1)

        def update_hotels(hotel_id):
            """
                Summary:
                    Update redis hotels dictionary
                Description:
                    Adjust the hotel frequency, Check if the hotel exists then add 1 to the current frequency value
                    or create a new hotel with frequency value = 1 if the user isn't exist
                Parameters:
                    hotel_id(str): hotel ID string
                Returns:
            """
            if self.rds.is_dict_key_exist(HOTELS_DICT_NAME, hotel_id):
                value = int(self.rds.get_from_dict(HOTELS_DICT_NAME, hotel_id))
                self.rds.insert_to_dict(HOTELS_DICT_NAME, hotel_id, value + 1)
            else:
                self.rds.insert_to_dict(HOTELS_DICT_NAME, hotel_id, 1)

        def update_advertisers(advertisers):
            """
                Summary:
                    Update redis advertisers dictionary
                Description:
                    For each advertiser in the advertisers list adjust the advertiser frequency,
                    Check if the advertiser exists then add 1 to the current frequency value
                    or create a new user with frequency value = 1 if the user isn't exist
                Parameters:
                    advertisers(list): A python list that represents the hotel advertisers
                Returns:
            """
            for advertiser in advertisers:
                if self.rds.is_dict_key_exist(ADVERTISERS_DICT_NAME, advertiser):
                    value = int(self.rds.get_from_dict(ADVERTISERS_DICT_NAME, advertiser))
                    self.rds.insert_to_dict(ADVERTISERS_DICT_NAME, advertiser, value + 1)
                else:
                    self.rds.insert_to_dict(ADVERTISERS_DICT_NAME, advertiser, 1)

        def update_hotels_min_offers(hotel_id, min_offer):
            """
                Summary:
                    Update redis hotels_min_offers dictionary
                Description:
                    Adjust the hotel minimum offer price ever seen per advertiser, If the hotel isn't in the dictionary then
                    creates a new hotel with minimum offer price equals to the current.
                    If the hotel exists then adjust the hotel unique advertisers list as long as 
                    the minimum offer price per advertisers. 
                Parameters:
                    hotel_id(str): hotel ID string
                    min_offer(dict): A python dictionary represents the min offer 
                    for this hotel among the hotel advertisers offers.
                    {
                        'advertiser': 'Booking.com',
                        'price': 12343 
                    }
                Returns:
            """
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
        """
        Summary:
            Run metrics flow
        Description:
            Run the full flow of the metrics calculation flow
        Parameters:
        Returns:
        """
        logger.info(msg=f'[MetricsFlow.run]: Run metrics calculation flow')
        self.init_redis_dicts()
        data = self.get_data()
        logger.info(msg='[MetricFlow.run]: Data being processed and update redis dictionaries')
        for message in data:
            self.update_metrics_dicts(message)
