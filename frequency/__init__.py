import os
from flask import Flask

"""EXPLAIN"""
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'Uploads'))

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "material lite is garbage"

from frequency import views

__version__ = '0.0.1'
