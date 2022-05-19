# -*- coding: utf-8 -*-
import json
from utilities.kafka_utility.configs import *
from kafka import KafkaProducer
from utilities.logging_utility import logger


class Producer:
    """
        Producer class to init a kafka producer
        Attributes:
            producer(KafkaProducer): A configured kafka producer object
    """
    def __init__(self, is_binary=True):
        logger.info(msg='[Producer.__init__]: ................ Init Kafka Producer ......................... ')
        """
            Summary:
                The producer class constructor
            Description:
                Init a kafka producer object with respect to is_binary parameter such that
                if it's True then get a producer with default value_serializer and that means
                tha data is formatted as byte object.
                If the is_binary parameter is False then create a producer with json value serializer
            Parameters:
                encoding(str): encoding scheme, default 'utf-8' and could be 'ascii'
                is_binary(bool): results in diff producers with diff value_serializers
        """
        self.producer = None
        if is_binary:
            self.producer = self._get_binary_producer()
        else:
            self.producer = self._get_json_producer()

    def _get_binary_producer(self):
        """
            Summary:
                Init a kafka producer
            Description:
               Init a kafka producer with respect to value_serializer
            Parameters:
            Returns:
                KafkaProducer: kafka producer instance
        """
        producer = KafkaProducer(
            bootstrap_servers=[BROKER_SERVER],
            api_version=API_VERSION,
            retries=RETRIES,
            # batch_size=5
            # linger_ms=GROUP_BATCHES_MILLISECONDS,
            # acks=ACKS
        )

        return producer

    def _get_json_producer(self):
        """
            Summary:
                Init a kafka producer
            Description:
               Init a kafka producer with respect to value_serializer = json
            Parameters:
            Returns:
                KafkaProducer: kafka producer instance
        """
        producer = KafkaProducer(
            bootstrap_servers=[BROKER_SERVER],
            api_versions=API_VERSION,
            retries=RETRIES,
            value_serializer=lambda v: json.dumps(v.encode(ENCODING)),
            # batch_size=5
            # linger_ms=GROUP_BATCHES_MILLISECONDS,
            # acks=ACKS
        )

        return producer

    def push_event_synchronously(self, message):
        # TODO: use the KafkaClient and SimpleProducer to send messages synchronously
        # The SimpleProducer has the send_messages function and it's sync by default
        # We can set the async=True flag to make it async
        # Note: KafkaProducer has the send function which is async by default
        pass

    def push_event_asynchronously(self, topic, message):
        """
            Summary:
                Push event to a specific kafka topic using the send method
            Description:
               Push a message to kafka topic, 'send()' by default is async, we can manipulate the send method
               based on the producer's different parameters mentioned above.
            Parameters:
                topic(str): The topic name
                message(bytes): A bytes object message to be sent to kafka
            Returns:
        """
        self.producer.send(
            topic=topic,
            value=message
        ).add_callback(
            self._on_send_success
        ).add_errback(
            self._on_send_failure
        )
        # To make all the buffered data available to sent even if 'linger_ms' greater than 0
        # self.producer.flush(timeout=10)

    def _on_send_success(self, record_metadata):
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

    def _on_send_failure(self, excp):
        # handle exception
        # log.error('I am an errback', exc_info=excp)
        print('I am an errback', excp)

    def push_to_topic(self, topic_name, message):
        """
        Summary:
            Push message to kafka topic
        Description:
            Push a byte object message to kafka topic
        Parameters:
            topic_name(str): Kafka topic name
            message(bytes): A bytes object message
        Returns:
        """
        logger.info(msg='[Producer.push_to_topic]: Start push message to kafka')
        future_record_metadata = self.producer.send(topic=topic_name, value=message)
        meta_data = future_record_metadata.get()
        if future_record_metadata.is_done:
            logger.info(msg=f'[Producer.push_to_topic]: A message has been successfully sent to kafka')
            if future_record_metadata.success:
                logger.info(msg=f'[Producer.push_to_topic]: A message has been successfully pushed to {meta_data.topic} kafka topic')
            else:
                logger.error(msg=f'[Producer.push_to_topic]: Failed to push a message to kafka')
        else:
            print("No Response")