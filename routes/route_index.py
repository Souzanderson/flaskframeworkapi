from flask.blueprints import Blueprint
from flask_cors import cross_origin

from handler.handlerIndex import HandlerIndex


route_index = Blueprint('route_index', __name__, template_folder='templates')
@route_index.route("/", methods = ["GET","POST","PUT","DELETE"])
@cross_origin(headers=["Content-Type", "Authorization"])
def index(): return HandlerIndex().handler()