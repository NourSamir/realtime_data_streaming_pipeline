# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC_NAME = os.getenv('KAFKA_RAW_DATA_TOPIC', '')

RAW_DATA_FILE_PATH = os.getenv('RAW_DATA_ASSET_FILE_PATH', 'producer_app/search_results_data.txt')
