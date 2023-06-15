from flask import Blueprint

bp = Blueprint('precios', __name__)


from app.precios import routes