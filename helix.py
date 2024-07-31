import os
from typing import Dict

import requests
from dotenv import load_dotenv

broadcaster_id = os.getenv("BROADCASTER_ID")
client_id = os.getenv("CLIENTE_ID")
secret_id = os.getenv("SECRET_TOKEN")
login_name = os.getenv("CLIENT_NAME")


class Credentials:

    def __init__(self):
        load_dotenv()
        self._access_token = None
        self._broadcaster_id = broadcaster_id
        self._client_id = client_id
        self._secret_id = secret_id
        self._login_name = login_name

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def broadcaster_id(self):
        return self._broadcaster_id

    @broadcaster_id.setter
    def broadcaster_id(self, value):
        self._broadcaster_id = value

    @property
    def secret_id(self):
        return self._secret_id

    @property
    def client_name(self):
        return self._login_name

    @property
    def client_id(self):
        return self._client_id


class Twitch:
    def __init__(self):
        self.credentials = Credentials()
        self.uri_helix = {
            "get_token": "https://id.twitch.tv/oauth2/token",
            "get_autorize": "https://id.twitch.tv/oauth2/autorize",
            "get_followers": "https://api.twitch.tv/helix/channels/followers",
            "get_users": "https://api.twitch.tv/helix/users",
            "get_editors": "https://api.twitch.tv/helix/channels/editors"
        }

        def get_params(self, **params: Dict[str, str]) -> Dict[str, str]:
            """
            :type params: Dict[str,str]
            :return Dict[str, str]
            """
            required_params = {
                "client_id": self.credentials.client_id,
                "client_secret": self.credentials.secret_id,
            }
            return {**required_params, **params}

    def get_header(self) -> Dict[str, str]:
        header = {
            "Client-Id": self.credentials.client_id,
            "Authorization": f"Bearer {self.credentials.access_token}",
        }
        return {**header}

    def get_access_token(self):
        try:
            response = requests.post(self.uri_token, data=self.get_params_access_token())
            json_response = response.json()
            self.credentials.access_token = json_response['access_token']
        except Exception as e:
            print(f"Error: {e}")

    def get_authorize(self):
        try:
            self.get_access_token()
            params = {
                "client_id": self.credentials.client_id,
                "redirect_uri": "https://127.0.0.1:5000/",
                "response_type": "code",
                "scope": "moderator:read:followers"
            }
            response = requests.get(self.uri_autorize, params=params)
            json_response = response.json()
            self.impr("response", json_response)
        except Exception as e:
            print(f"Error: {e}")

    def get_latest_follower(self):
        params = {"broadcaster_id": self.credentials.broadcaster_id, "scopes": "moderator:read:followers"}
        response = requests.get(self.uri_followers, headers=self.get_header(), params=params).json()
        return response

    def get_channel_editors(self):
        params = {"broadcaster_id": self.credentials.client_id}
        headers = self.get_header()
        response = requests.get(self.uri_editors, headers=headers, params=params).json()
        return response

    def get_brodcaster_id(self):
        params = {"login": self.credentials.client_name}
        response = requests.get(self.uri_users, headers=self.get_header(), params=params).json()
        self.credentials.broadcaster_id = response['data'][0]["id"]

    def impr(self, text, variable):
        print(f"----- {text} -----")
        print(variable)
