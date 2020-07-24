from flask_restx import Api

from .tweet_services import api_ns
from .oauth1_services import oauth1_ns

api = Api(title="Databox Tweeter API", version="1.0", description="A simple demo API",)
# api.add_namespace(api_ns)
api.add_namespace(oauth1_ns)
