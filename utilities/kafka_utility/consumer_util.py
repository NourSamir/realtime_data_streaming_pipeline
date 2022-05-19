# -*- coding: utf-8 -*-

import json
from utilities.logging_utility import logger
from utilities.kafka_utility.configs import *
from kafka import KafkaConsumer


class Consumer:
    """
        Consumer class to init a kafka consumer
        Attributes:
            consumer(KafkaConsumer): A configured kafka consumer object
            is_binary(bool): A flag to tell us about the desrializer
    """
    def __init__(self, is_binary=True):
        logger.info(msg='[Consumer.__init__]: ................ Init Kafka Consumer ......................... ')
        """
            Summary:
                The Consumer class constructor
            Description:
                Init a kafka consumer object with respect to is_binary parameter such that
                if it's True then get a consumer with default value_deserializer and that means
                tha data is formatted as byte object.
                If the is_binary parameter is False then create a producer with json value deserializer
            Parameters:
                is_binary(bool): results in diff producers with diff value_serializers
        """
        self.consumer = None
        self.is_binary = is_binary
        if is_binary:
            self.consumer = self._get_binary_consumer()
        else:
            self.consumer = self._get_json_consumer()

    def _get_binary_consumer(self):
        """
            Summary:
                Init a kafka consumer
            Description:
               Init a kafka consumer with respect to value_deserializer
            Parameters:
            Returns:
                KafkaConsumer: kafka consumer instance
        """
        consumer = KafkaConsumer(
            # topic_name,
            bootstrap_servers=[BROKER_SERVER],
            group_id=CONSUMER_GROUP_ID,
            enable_auto_commit=AUTO_COMMIT,
            auto_commit_interval_ms=OFFSET_COMMIT_INTERVAL,
            auto_offset_reset=OFFSET_RESET
        )

        return consumer

    def _get_json_consumer(self):
        """
            Summary:
                Init a kafka consumer
            Description:
               Init a kafka consumer with respect to value_deserializer = json
            Parameters:
            Returns:
                KafkaConsumer: kafka consumer instance
        """
        consumer = KafkaConsumer(
            # topic_name,
            bootstrap_servers=[BROKER_SERVER],
            group_id=CONSUMER_GROUP_ID,
            enable_auto_commit=AUTO_COMMIT,
            auto_commit_interval_ms=OFFSET_COMMIT_INTERVAL,
            auto_offset_reset=OFFSET_RESET,
            value_deserializer=lambda v: json.loads(v.decode(ENCODING))
        )

        return consumer

    def consume(self, topics):
        logger.info(msg=f'[Consumer.consume]: Start consuming messages from {topics} topics')
        """
            Summary:
                Consume message from a topic
            Description:
               Manually subscribe to a list of topics to read messages from using
               the pre-configured consumer.
            Parameters:
                topics(list): a list of topic's names
            Returns:
        """
        self.consumer.subscribe(topics)
        for message in self.consumer:
            # print(message.topic, message.partition, message.offset, message.timestamp, message.key, message.value)
            if self.is_binary:
                yield json.loads(message.value)
            else:
                yield message

