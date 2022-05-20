# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

# Broker server url
# BROKER_SERVER = 'localhost:9092'
BROKER_SERVER = os.getenv('KAFKA_BROKER_SERVER', 'localhost:9092')

# API version
# API_VERSION = (0, 10, 1)
api_version = os.getenv('KAFKA_API_VERSION', (0, 10, 1))
v_part_1, v_part_2, v_part_3 = api_version.split(',')
API_VERSION = (int(v_part_1), int(v_part_2), int(v_part_3)) if type(api_version) is str else api_version

# Producer number of retries
RETRIES = int(os.getenv('KAFKA_RETRIES', 5))

# Could be 'ascii'
ENCODING = os.getenv('KAFKA_ENCODING', 'utf-8')

# 'batch_size' parameter to determine the number of records to be batched
# by the producer and sent in once.
BATCH_SIZE = os.getenv('KAFKA_BATCH_SIZE', 10)

# Do a smart grouping using a smart delay via the 'linger_ms' parameter to group the records
# that arrive within a certain amount of milliseconds.
GROUP_BATCHES_MILLISECONDS = os.getenv('KAFKA_GROUP_BATCHES_MILLISECONDS', 5)

# We can use the 'acks' parameter, it's the number of acknowledgments the producer requires
# before considering a request complete. This controls the durability of record
ACKS = os.getenv('KAFKA_ACKS', 'all')

# Commit the consumer offset every N milliseconds in the background
AUTO_COMMIT = True if os.getenv('KAFKA_AUTO_COMMIT') == 'true' else False

# Tell the consumer from where to start
# 'earliest': Will move to the most recent, wait and listens to new messages
# 'latest': Start from the begining every time that can double processes the old messages
OFFSET_RESET = os.getenv('KAFKA_OFFSET_RESET', 'latest')

# Default value is 5000 ms, we can change it
OFFSET_COMMIT_INTERVAL = int(os.getenv('KAFKA_OFFSET_COMMIT_INTERVAL', 5000))

# Assign the consumer to a group because of the dynamic partitioning
CONSUMER_GROUP_ID = os.getenv('KAFKA_CONSUMER_GROUP_ID', 'consumer_group_1')

# Topic to consume messages from and producer to, we can set many topics for the same consumer
RAW_DATA_TOPIC_NAME = os.getenv('KAFKA_RAW_DATA_TOPIC', 'raw_events')

PROCESSED_DATA_TOPIC_NAME = os.getenv('KAFKA_PROCESSED_DATA_TOPIC', 'processed_events')
