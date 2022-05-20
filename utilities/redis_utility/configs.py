# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

REDIS_PORT = os.getenv('REDIS_PORT', 6379)

REDIS_DB = os.getenv('REDIS_DB', 0)

REDIS_PASSWORD = None if os.getenv('REDIS_PASSWORD') == 'None' else ''
