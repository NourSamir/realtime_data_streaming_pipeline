# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

# REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

REDIS_HOST = 'host.docker.internal'

REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

REDIS_DB = int(os.getenv('REDIS_DB', 0))

REDIS_PASSWORD = None if os.getenv('REDIS_PASSWORD') == 'None' else ''

REDIS_DICT_NAMES = [
	'hotels_min_offers',
	'advertisers',
	'hotels',
	'users'
]