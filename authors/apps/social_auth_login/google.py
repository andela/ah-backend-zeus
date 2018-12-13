import os
from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info

        :param str auth_token: The access token of the Google user
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            user_id = idinfo['sub']
            return idinfo
        except ValueError:
            return "The token is either invalid or has expired"
