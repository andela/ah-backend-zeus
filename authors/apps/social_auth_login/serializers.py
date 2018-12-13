from rest_framework import serializers
from authors.apps.social_auth_login import facebook, google, twitter_auth
from authors.apps.social_auth_login.register import register_facebook_user, register_google_user, register_twitter_user


class FacebookSocialAuthViewSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = facebook.Facebook.validate(auth_token)
        try:
            user_data['id']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        user_id = user_data['id']
        email = user_data['email']
        name = user_data['name']

        return register_facebook_user(user_id=user_id, email=email, name=name)


class GoogleSocialAuthViewSerializer(serializers.Serializer):
    """Handles serialization of google related data"""

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']

        return register_google_user(user_id=user_id, email=email, name=name)


class TwitterAuthViewSerializer(serializers.Serializer):
    """Handles serialization of twitter related data"""

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_info = twitter_auth.TwitterAuthTokenVerification.validate_twitter_auth_tokens(
            auth_token)
        try:
            user_info['id_str']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        user_id = user_info['id_str']
        email = user_info['email']
        name = user_info['name']

        return register_twitter_user(user_id=user_id, email=email, name=name)
