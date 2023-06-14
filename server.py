from flask import Flask 
from flask_cors import CORS

from routes import *

app = Flask(__name__)

cors = CORS(app, resources={r"/": {"origins": "*.*"}})
app.config['MAX_CONTENT_LENGTH'] = 1600 * 1024 * 1024

app.register_blueprint(route_index)
