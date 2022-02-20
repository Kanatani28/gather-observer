import requests
import json

class DiscordClient:
    
    def __init__(self, token, channel_id):
        self.channel_id = channel_id
        self.token = token
        pass
    
    def send_message(self, data):
        headers = {
            'Authorization': f'Bot {self.token}',
            'content-type': 'application/json'
        }
        url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages'
        res = requests.post(url, headers=headers, data=json.dumps(data))
        print(res)