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


user_response = oauth1_ns.model('user_response', {
    'id_str':fields.String(description='id_str'),
    'screen_name':fields.String(description='screen_name'),
    'location':fields.String(description='location'),
    'friends_count':fields.Integer(description='friends_count'),
    'followers_count': fields.Integer(description='followers_count')

})

user_responses = oauth1_ns.model('user_responses', {
    'users':fields.List(fields.Nested(user_response))
})


#TODO
# flask_restx.fields.MarshallingError: Unable to marshal field "created_at" value "Wed Jul 15 17:00:46 +0000 2020": Invalid date literal "Wed Jul 15 17:00:46 +0000 2020"
tweet_response = oauth1_ns.model('tweet_response', {
    'created_at':fields.String(description='created_at'),
    'id_str':fields.String(description='id_str'),
    'text':fields.String(description='text'),
    'source':fields.String(description='source'),
    'retweet_count': fields.Integer(description='retweet_count'),
    'favorite_count': fields.Integer(description='favorite_count')

})

tweet_responses = oauth1_ns.model('tweet_responses', {
    'events':fields.List(fields.Nested(tweet_response))
})

message_data = oauth1_ns.model('message_data', {
    'text':fields.String(description='created_at')
})

message_create = oauth1_ns.model('message_create', {
    'sender_id':fields.String(description='created_at'),
    'message_data': fields.Nested(message_data)
})

dm_response = oauth1_ns.model('dm_response', {
    'id':fields.String(description='created_at'),
    'created_timestamp':fields.String(description='id_str'),
    'message_create': fields.Nested(message_create)
})

dm_responses = oauth1_ns.model('dm_responses', {
    'events':fields.List(fields.Nested(dm_response))
})

show_parser = oauth1_ns.parser()
show_parser.add_argument('screen_name', type=str);


@oauth1_ns.route('/list_followings/')
class Token(Resource):

    @oauth1_ns.doc('Listing followings')
    @oauth1_ns.marshal_with(user_responses, code=http.client.OK)
    def get(self):
        '''list followings'''

        response = services.list_followings()

        oauth1_ns.logger.debug("response {}".format(response))

        return response

@oauth1_ns.route('/list_followers/')
class Token(Resource):

    @oauth1_ns.doc('Listing followers')
    @oauth1_ns.marshal_with(user_responses, code=http.client.OK)
    def get(self):
        '''list followers'''

        response = services.list_followers()

        oauth1_ns.logger.debug("response {}".format(response))

        return response

@oauth1_ns.route('/show/')
@oauth1_ns.expect(show_parser)
class SearchTweets(Resource):

    @oauth1_ns.doc('Show user')
    @oauth1_ns.marshal_with(user_response, code=http.client.OK)
    def get(self):
        '''show user'''

        params = show_parser.parse_args()

        oauth1_ns.logger.debug("args {}".format(params))

        response = services.show_user(params['screen_name'])

        oauth1_ns.logger.debug("response {}".format(response))

        return response

@oauth1_ns.route('/list_retweets/')
class Token(Resource):

    @oauth1_ns.doc('Listing statuses of retweets_of_me')
    @oauth1_ns.marshal_with(tweet_response, code=http.client.OK)
    def get(self):
        '''list statuses of retweets_of_me'''

        response = services.list_retweets()

        oauth1_ns.logger.debug("response {}".format(response))

        return response



@oauth1_ns.route('/list_favorites/')
class Token(Resource):

    @oauth1_ns.doc('Show the tweets which I liked')
    @oauth1_ns.marshal_with(tweet_response, code=http.client.OK)
    def get(self):
        '''favorites are now known as likes'''

        response = services.list_likes()

        oauth1_ns.logger.debug("response {}".format(response))

        return response


@oauth1_ns.route('/list_mentions/')
class Token(Resource):

    @oauth1_ns.doc('Show the tweets where I mentioned')
    @oauth1_ns.marshal_with(tweet_response, code=http.client.OK)
    def get(self):
        '''favorites are now known as likes'''

        response = services.list_mentions()

        oauth1_ns.logger.debug("response {}".format(response))

        return response

@oauth1_ns.route('/show_dms/')
class Token(Resource):

    @oauth1_ns.doc('Show DMs')
    @oauth1_ns.marshal_with(dm_responses, code=http.client.OK)
    def get(self):
        '''Returns all Direct Message events (both sent and received) within the last 30 days. Sorted in reverse-chronological order.'''

        response = services.list_dms()

        oauth1_ns.logger.debug("response {}".format(response))

        return response


@oauth1_ns.route('/list_user_tweets/')
class Token(Resource):

    @oauth1_ns.doc('Show the tweets posted by user')
    @oauth1_ns.marshal_with(tweet_response, code=http.client.OK)
    def get(self):
        '''favorites are now known as likes'''

        response = services.list_user_tweets()

        oauth1_ns.logger.debug("response {}".format(response))

        return response