import os
from flask import Flask
from redis import StrictRedis

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'Uploads'))
CACHE_NAME = 'word_cache'
CACHE_KEY = 'word_tree'
REDIS_URL = 'redis://localhost:6379'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CACHE_NAME'] = CACHE_NAME
app.config['CACHE_KEY'] = CACHE_KEY
app.config['REDIS_URL'] = REDIS_URL
app.secret_key = "material lite is garbage"


redis_conn = StrictRedis.from_url(REDIS_URL)

from app import views

__version__ = '0.0.1'
