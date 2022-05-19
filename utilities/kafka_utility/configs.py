# -*- coding: utf-8 -*-

# Broker server url
BROKER_SERVER = 'localhost:9092'

# API version
API_VERSION = (0, 10, 1)

# Producer number of retries
RETRIES = 5

# Could be 'ascii'
ENCODING = 'utf-8'

# 'batch_size' parameter to determine the number of records to be batched
# by the producer and sent in once.
BATCH_SIZE = 10

# Do a smart grouping using a smart delay via the 'linger_ms' parameter to group the records
# that arrive within a certain amount of milliseconds.
GROUP_BATCHES_MILLISECONDS = 5

# We can use the 'acks' parameter, it's the number of acknowledgments the producer requires
# before considering a request complete. This controls the durability of record
ACKS = 'all'

# Commit the consumer offset every N milliseconds in the background
AUTO_COMMIT = True

# Tell the consumer from where to start
# 'earliest': Will move to the most recent, wait and listens to new messages
# 'latest': Start from the begining every time that can double processes the old messages
OFFSET_RESET = 'latest'

# Default value is 5000 ms, we can change it
OFFSET_COMMIT_INTERVAL = 30 * 1000

# Assign the consumer to a group because of the dynamic partitioning
CONSUMER_GROUP_ID = 'consumer_group_1'

# Topic to consume messages from and producer to, we can set many topics for the same consumer
RAW_DATA_TOPIC_NAME = 'raw_events'
PROCESSED_DATA_TOPIC_NAME = 'processed_events'
