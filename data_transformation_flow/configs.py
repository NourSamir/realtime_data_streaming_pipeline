# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_INPUT_TOPICS = [os.getenv('KAFKA_RAW_DATA_TOPIC', '')]

KAFKA_OUTPUT_TOPIC = os.getenv('KAFKA_PROCESSED_DATA_TOPIC', 'processed_events')