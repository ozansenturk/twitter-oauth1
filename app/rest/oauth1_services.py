from flask_restx import Namespace, Resource, fields
import http.client
from app.backend import services
import logging


logging.basicConfig(level=logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(
                 '%(asctime)s %(levelname)s: %(message)s '
                 '[in %(pathname)s:%(lineno)d]'))

oauth1_ns = Namespace('api', description='Twitter management')

oauth1_ns.logger.addHandler(stream_handler)

token_request = oauth1_ns.model('token_request', {
    'client_id':fields.String(description='Twiter API Key'),
    'client_secret':fields.String(description='Twitter API Secret')
})

user_response = oauth1_ns.model('user_response', {
    'id_str':fields.String(description='id_str'),
    'screen_name':fields.String(description='screen_name'),
    'location':fields.String(description='location'),
    'friends_count':fields.Integer(description='location')
})

user_response = oauth1_ns.model('user_response', {
    'id_str':fields.String(description='id_str'),
    'screen_name':fields.String(description='screen_name'),
    'location':fields.String(description='location'),
    'friends_count':fields.Integer(description='location')
})

user_responses = oauth1_ns.model('user_responses', {
    'users':fields.List(fields.Nested(user_response))
})

@oauth1_ns.route('/list_users/')
class Token(Resource):

    @oauth1_ns.doc('Listing users')
    @oauth1_ns.marshal_with(user_responses, code=http.client.OK)
    def get(self):
        '''Get tweets'''

        response = services.list_users()

        oauth1_ns.logger.debug("response {}".format(response))

        return response



