import json
from data_transformation_flow.configs import *
from utilities.logging_utility import logger
from utilities.kafka_utility.consumer_util import Consumer
from utilities.kafka_utility.producer_util import Producer

class TransformationFlow:
    """
        Processor class to consume data messages from input_data_topics, process
        the consumed messages and produce the processed messages to output_data_topics
        Attributes:
            data_consumer(Consumer): A kafka consumer object
            data_producer(Producer): A kafka producer object
    """
    def __init__(self):
        logger.info(msg='[Processor.__init__]: Init the consumer and producer objects')
        """
            Summary:
                The Processor class constructor
            Description:
                Init a kafka consumer and producer
            Parameters:
                input_data_topics(list): A list of input topics to consume data from
                output_data_topic(str): The output topic name to producer the processed data to
        """
        self.data_consumer = Consumer()
        self.data_producer = Producer()

    def get_raw_data(self):
        """
            Summary:
                Run the consumer to start listening to the input_topics
            Description:
                Run the consumer and start listening to the input_topics and fetch the newly arrived messages
            Parameters:
            Returns:
                dict: A consumed message as python dictionary
        """
        for message in self.data_consumer.consume(KAFKA_INPUT_TOPICS):
            yield message

    def process(self, raw_message_data):
        """
            Summary:
                Process the raw message
            Description:
                Process and transform the raw message data to obtain more insights,
                in our case we obtain a list of the hotel search advertisers and
                the minimum price ever offer for this hotel by the advertisers
            Parameters:
                raw_message_data(dict): A python dictionary represents the user's hotel search
            Returns:
                dict: A python dictionary that represents the processed message with the newly added fields
        """
        processed_message_data = dict()
        hotel_advertisers_list = []
        min_offer = {
            'price': 1e18,
            'advertiser': ''
        }

        hotel_advertisers = raw_message_data['hotel_advertisers']
        for advertiser, advertiser_offers in hotel_advertisers.items():
            hotel_advertisers_list.append(advertiser)
            advertiser_min_offer = self._get_min_offer(advertiser_offers)
            if advertiser_min_offer < min_offer['price']:
                min_offer['price'] = advertiser_min_offer
                min_offer['advertiser'] = advertiser

        processed_message_data['user_id'] = raw_message_data['user_id']
        processed_message_data['hotel_id'] = raw_message_data['hotel_id']
        processed_message_data['search_timestamp'] = raw_message_data['search_timestamp']
        processed_message_data['advertisers'] = hotel_advertisers_list
        processed_message_data['min_offer'] = min_offer

        return processed_message_data

    def push_processed_data(self, processed_message_data):
        """
            Summary:
                Push to output topic
            Description:
                Push processed and transformed message to output topic
            Parameters:
                processed_message_data(dict): A python dictionary represents the processed message
            Returns:
        """
        self.data_producer.push_to_topic(
            topic_name=KAFKA_OUTPUT_TOPIC,
            message=bytes(json.dumps(processed_message_data), encoding='utf-8')
        )

    def _get_min_offer(self, offers):
        """
            Summary:
                Get minimum offer price
            Description:
                Get the minimum offer price from offers list such that each offer is a dict
            Parameters:
                offers(list): A python list of dictionaries represents the offers list
            Returns:
                int: The minimum price
        """
        min_offer = 1e18
        for offer in offers:
            min_offer = min(min_offer, offer['eurocents'])

        return min_offer

    def run(self):
        """
            Summary:
                Run the full processor ETL
            Description:
                Run the consumer to fetch the data, invoke the process function to be applied to
                each message that arrives and run the producer to push the transformed message to
                the destination topic.
            Parameters:
            Returns:
        """
        logger.info(msg=f'[Processor.run]: Start fetching messages from {KAFKA_INPUT_TOPICS}')
        raw_data = self.get_raw_data()
        logger.info(msg=f'[Processor.run]: Start processing messages and push it to {KAFKA_OUTPUT_TOPIC}')
        for raw_data_message in raw_data:
            processed_data_message = self.process(raw_data_message)
            self.push_processed_data(processed_data_message)
