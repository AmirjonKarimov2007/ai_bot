# Made by Jaloliddin!!

import requests
import json

def get_response_from_server(history):
    url = 'http://gptserver.alwaysdata.net/get_response'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "history": history
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        return {"error": f"Request failed with status code {response.status_code}"}


