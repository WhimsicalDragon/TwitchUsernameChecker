import requests
import config

def pushDiscordMessage(message):


    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'content': message,
    }

    response = requests.post(config.WEBHOOKURL, headers=headers, json=json_data)