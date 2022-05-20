# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC_NAME = os.getenv('KAFKA_RAW_DATA_TOPIC', '')

