# twitter oauth1 and oauth2 implementations

#Installation
place an env. file into the root directory within the content below

Directory structure
```python
├── README.md
├── app
│   ├── __init__.py
│   ├── backend
│   │   ├── __init__.py
│   │   └── services.py
│   ├── rest
│   │   ├── __init__.py
│   │   ├── oauth1_services.py
│   │   └── tweet_services.py
│   ├── static
│   │   ├── dm.json
│   │   └── user.json
│   ├── templates
│   │   ├── base.html
│   │   ├── callback-success.html
│   │   ├── error.html
│   │   ├── index.html
│   │   └── start.html
│   └── views
│       ├── __init__.py
│       └── auth.py
├── config.py
├── http.ini
├── requirements.txt
└── wsgi.py


```
Envrionment variables
```.env
API_KEY="*******"
API_SECRET_KEY="*******"

BASE_URL = "https://api.twitter.com/"

URL_AUTH="oauth2/token"
URL_SEARCH="1.1/search/tweets.json"

CALL_BACK_URL='********/callback'

API_LIST_FRIENDS="https://api.twitter.com/1.1/friends/list.json"
API_LIST_FOLLOWERS="https://api.twitter.com/1.1/followers/list.json"
API_SHOW_USER="https://api.twitter.com/1.1/users/show.json"
API_LIST_RETWEETS="https://api.twitter.com/1.1/statuses/retweets_of_me.json"
API_LIST_FAVORITES="https://api.twitter.com/1.1/favorites/list.json"
API_LIST_MENTIONS="https://api.twitter.com/1.1/statuses/mentions_timeline.json"
API_LIST_DMS="https://api.twitter.com/1.1/direct_messages/events/list.json"
API_LIST_USER_TWEETS="https://api.twitter.com/1.1/statuses/user_timeline.json"
```

Installation
```python
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uwsgi http.ini



