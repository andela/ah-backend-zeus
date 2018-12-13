import facebook


class Facebook:
    """Facebook class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info

        :param str auth_token: The access token of the facebook user
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token, version="3.0")
            profile = graph.request('/me?fields=id,name,email')
            return profile
        except:
            message = "The token is invalid or expired."
            return message
