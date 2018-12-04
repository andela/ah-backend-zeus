import re
from rest_framework import serializers


def validate_registration(data):
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    if (not username and not email and not password):
        raise serializers.ValidationError(

            {

            'input fields':
            'Please all input fields are required'   
            }

        )
    
    if len(username) < 4:
        raise serializers.ValidationError(
            {
                'username':
                'Please the username should be at least 4 characters long and above'
            }
        )
    
    if not re.match(r"^[A-Za-z]+[\d\w_]+", username):
        raise serializers.ValidationError(

            {

            'username':
            'Username should start with letters'+' and sometimes include underscores and numbers'    
            }
        )

    if not re.search(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        raise serializers.ValidationError(
                {
                'Email':
                'Please enter a valid email address'

                }
        )
    
    valid_password(password)
    return{"username": username, "email": email, "password": password}

def valid_password(password):
    long_password = (len(password)>7)
    atleast_number = re.search("[0-9]", password)
    Capital_letters = re.search("[A-Z]", password)

    if (not long_password or not atleast_number or not Capital_letters):
        raise serializers.ValidationError(

            {

                'password':
                'Weak password: password should contain'+ 
                ' at least 8 characters long ' + ',' + 'capital letter and a number'
            }

        )

     

        