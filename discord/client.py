import requests

class DiscordClient:
    
    def __init__(self, token, channel_id):
        self.channel_id = channel_id
        self.token = token
        pass
    
    def send_message(self, embeds):
        headers = {'Authorization': f'Bot {self.token}'}
        url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages'
        requests.post(url, headers=headers, data={"embeds": embeds})