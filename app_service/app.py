from flask import Flask
from flask_cors import CORS
from utilities.redis_utility.redis_util import RedisUtility

# Init the flask app
app = Flask(__name__)
CORS(app)
app.debug = True

# Init a DB session
redis_session = RedisUtility()
