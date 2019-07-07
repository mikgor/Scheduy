import json
import requests
from Scheduy.local_settings import *

class MessengerApiHandler:
    def SendResponseMessage(self, recipient, message):
        payload = {'messaging_type': 'RESPONSE', 'recipient': {'id': str(recipient)}, 'message': {'text': str(message), 'quick_replies': [
        {'content_type': 'text', "title":"Enable notifications","payload":"<ENABLE_PAYLOAD>",},
        {'content_type': 'text', "title":"Disable notifications","payload":"<DISABLE_PAYLOAD>",},
        {'content_type': 'text', "title":"Help","payload":"<HELP_PAYLOAD>"}]}}
        return requests.post("https://graph.facebook.com/v3.3/me/messages?access_token="+MESSENGER_API_KEY, json=payload)

    def SendAutoResponseMessage(self, recipient, message):
        messages = {
            "hi": "Hello.",
            "how are you?": "I'm fine. Thank you.",
            "help": "If you want to enable Messenger notifications click 'Enable notifications' below. You can disable notifications at any time using 'Disable notifications'."
        }
        answer = ""
        if message in messages:
            answer = messages[message]
        else:
            answer = "I don't understand this message. Try HELP for more information."
        return self.SendResponseMessage(recipient, answer)

    def SendConnectMessage(self, recipient, token):
        return self.SendResponseMessage(recipient, "Click the link below to connect your Scheduy account with Messenger in order to enable notifications. You can disable it at any time. This link expires in 10 minutes. After expired you can generate new one using Connect button. http://185.238.75.128/connectmessenger/?token="+str(token))

    def SendNotificationMessage(self, recipient, message):
        payload = {'messaging_type': 'MESSAGE_TAG', 'tag': 'CONFIRMED_EVENT_REMINDER', 'recipient': {'id': str(recipient)}, 'message': {'text': str(message), 'quick_replies': [
        {'content_type': 'text', "title":"Enable notifications","payload":"<ENABLE_PAYLOAD>",},
        {'content_type': 'text', "title":"Disable notifications","payload":"<DISABLE_PAYLOAD>",},
        {'content_type': 'text', "title":"Help","payload":"<HELP_PAYLOAD>"}]}}
        return requests.post("https://graph.facebook.com/v3.3/me/messages?access_token="+MESSENGER_API_KEY, json=payload)
