from flask import Flask

"""EXPLAIN"""

app = Flask(__name__, static_url_path='/static')

from frequency import frequency

__version__ = '0.0.1'
