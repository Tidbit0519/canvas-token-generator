import webbrowser
import requests
import json
import os
from dotenv import dotenv_values, load_dotenv

config = dotenv_values(".env")

def request_canvas_access(client_id, redirect_uri):
    canvas_url = config['CANVAS_URL'] + "/login/oauth2/auth"
    auth_url = f"{canvas_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    webbrowser.open(auth_url)

def get_authorization_code():
    code = input("Enter the authorization code: ")
    return code

def get_access_token(client_id, client_secret, code, redirect_uri):
    token_url = "https://byuh.test.instructure.com/login/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code
    }
    response = requests.post(token_url, data=payload)
    return response.json()  # Contains access_token

def access_canvas_api(access_token):
    url = "https://byuh.test.instructure.com/api/v1/courses/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()  # Contains the data from Canvas API

client_id = config['CLIENT_ID']
client_secret = config['CLIENT_SECRET']
redirect_uri = config['REDIRECT_URI']

# Step 1: User initiates OAuth flow
request_canvas_access(client_id, redirect_uri)

# Step 2: User enters the code they receive after authorization
code = get_authorization_code()

# Step 3: Exchange code for an access token
token_response = get_access_token(client_id, client_secret, code, redirect_uri)
access_token = token_response.get('access_token')

# Step 4: Use the access token to access Canvas API
api_response = access_canvas_api(access_token)
json_str = json.dumps(api_response, indent=4)
print(api_response)
