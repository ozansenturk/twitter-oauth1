from flask import Flask, Blueprint

views_v1 = Blueprint('views', __name__)

from . import auth
