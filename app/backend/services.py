import requests
import json
from flask import current_app
import datetime
import os
import os.path
from datetime import timedelta
import base64
from flask import current_app
import oauth2 as oauth
from app.views.auth import user_credentials
import ast

def get_current_year(date_str):

    datee = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    return datee.year

def get_current_month(date_str):

    datee = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    return datee.month


def split_column(x):

    if x:
        temp = x.split('_')
        return int(temp[0]), temp[1]
    else:
        return None, None


def check_whether_file_older(file_name, delta_minutes):

    minutes_ago = datetime.datetime.now() - timedelta(minutes=delta_minutes)
    filetime = datetime.datetime.fromtimestamp(os.path.getctime(file_name))

    if filetime < minutes_ago:
        current_app.logger.debug("file created {} minutes ago".format(filetime))
        return True
    else:
        return False




def prepare_header(client_id, client_secret):

    key_secret ='{}:{}'.format(client_id, client_secret).encode('ascii')

    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    auth_headers = {
        # 'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    return auth_headers


def post_query(service_endpoint, data, headers=None, params=None):
    """

    :param url:
    :param data:
    :param params:
    :return:
    """
    base_url = os.environ.get("BASE_URL")

    response = requests.post("{}{}".format(base_url,service_endpoint), data=data, headers=headers, params=params)

    # current_app.logger.debug("Response: {} ".format(response.json()))

    return response

def get_query(service_endpoint, headers=None, params=None):
    """

    :param url:
    :param data:
    :param params:
    :return:
    """
    base_url = os.environ.get("BASE_URL")

    response = requests.get("{}{}".format(base_url,service_endpoint), headers=headers, params=params)

    # current_app.logger.debug("Response: {} ".format(response.json()))

    return response


def get_bearer_token(client_id=None, client_secret=None):

    if (client_id is None) & (client_secret is None):
        client_id=os.environ.get("API_KEY")
        client_secret=os.environ.get("API_SECRET_KEY")

    auth_url = os.environ.get("URL_AUTH")

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_headers = prepare_header(client_id, client_secret)

    auth_resp = post_query(auth_url, auth_data, auth_headers)

    return auth_resp


def search_tweets(params):

    search_url = os.environ.get("URL_SEARCH")

    #TODO caching and add before request decorater
    bearer_token = get_bearer_token()
    access_token = bearer_token.json()['access_token']

    auth_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    auth_resp = get_query(search_url, auth_headers, params)

    return auth_resp

def list_users():

    search_url = os.environ.get("URL_SEARCH")

    consumer = oauth.Consumer(
        current_app.config['APP_CONSUMER_KEY'], current_app.config['APP_CONSUMER_SECRET'])

    # real_token = oauth.Token(user_credentials['real_oauth_token'], user_credentials['real_oauth_token_secret'])
    real_token = oauth.Token('769594983280177153-9zO8kqfBARawPrjKVal1a6jp2WYw2Pc',
                             'jtuf7uEvzBOjD1u708sZvcEXJVuNi0ChiFwguWoUh9f7b')

    real_client = oauth.Client(consumer, real_token)

    #token
    #token secret

    real_resp, real_content = real_client.request(
        os.environ.get("API_LIST_FRIENDS") , "GET")

    dict_str = real_content.decode("UTF-8")
    json_content = json.loads(dict_str)

    return json_content