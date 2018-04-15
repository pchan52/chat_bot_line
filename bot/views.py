from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
import json
import requests

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 's1QnhL2/aBnNeuGpbaQMgzCTw0jSs3d8Yun+CXQs0mjX/Z60qiKcuNn2N76OjWVydkXuez9o4Dc8s9zLKZTwwsNbyYB9IjKg9joidEVTpeQe7jTTevQ/90zrrr4D6HfJiM6zHPT6lX/zULN9m0BlrgdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def reply_text(reply_token, text):
    reply = "reply"
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    return reply

def reply_text_watson(reply_token, text):
    import watson_developer_cloud

    print(text)

    assistant = watson_developer_cloud.AssistantV1(
        username='150c843f-ce7e-4751-8a5f-148d111972ee',
        password='coYNA700SQui',
        version='2018-02-16'
    )

    from watson_developer_cloud import WatsonApiException
    try:
        # Invoke a Assistant method
        response = assistant.message(
            workspace_id='585d1384-6b78-42a3-8911-5958572af8a4',
            input={
                'text': 'Hello'
            }
        )
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)

    print(json.dumps(response, indent=2))

    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": response["output"]["text"][0]
            }
        ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    return response["output"]["text"][0]


def index(request):
    return HttpResponse("this is bot api")


def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8'))
    for e in request_json['events']:
        reply_token = e['replyToken']
        message_type = e['message']['type']

        if message_type == 'text':
            text = e['message']['text']
            reply += reply_text_watson(reply_token, text)
    return HttpResponse(reply)