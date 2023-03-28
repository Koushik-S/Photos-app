import json
import boto3
from botocore.vendored import requests
from requests_aws4auth import AWS4Auth
from utils import *
import datetime
import json
import os
import requests

import boto3
# Define the client to interact with Lex
client = boto3.client('lexv2-runtime')
def lambda_handler(event, context):
    print(event)
    print(context)
    # msg_from_user = event['messages'][0]['unstructured']['text']
    # print(msg_from_user)

def lambda_handler(event, context):
    """
    Param: labels is list of keywords: str
    Return a list of photos, each photo is a dict like
    
    """
    # query = event['q']
    # print(event)
    # print(query)

    #user_id = generate_id()
    response = client.recognize_text(
            botId='THGAWADSYH', # MODIFY HERE
            botAliasId='H6XM2RZQ5G', # MODIFY HERE
            localeId='en_US',
            sessionId='testuser3',
            text="Show me pictures of cat")
    print(response)
    # {'ResponseMetadata': {'RequestId': 'c79517e8-eb90-41ff-a1db-654099033dd4', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'date': 'Thu, 30 Apr 2020 00:49:38 GMT', 'x-amzn-requestid': 'c79517e8-eb90-41ff-a1db-654099033dd4', 'content-length': '291', 'connection': 'keep-alive'}, 'RetryAttempts': 0}, 
    # 'intentName': 'SearchIntent', 'slots': {'objects': 'cats'}, 'message': 'cats', 'messageFormat': 'PlainText', 'dialogState': 'Fulfilled', 'sessionId': '2020-04-30T00:49:38.326Z-MQYjLhNz'}
    
    # {'ResponseMetadata': {'RequestId': '2994cb3c-1d32-4295-bc6a-b5fe7d0bf77e', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'date': 'Thu, 30 Apr 2020 03:58:14 GMT', 'x-amzn-requestid': '2994cb3c-1d32-4295-bc6a-b5fe7d0bf77e', 'content-length': '313', 'connection': 'keep-alive'}, 'RetryAttempts': 0}, 
    # 'intentName': 'SearchIntent', 'slots': {'objects': 'cats', 'objects_two': 'dogs'}, 'dialogState': 'ReadyForFulfillment', 'sessionId': '2020-04-30T03:58:14.298Z-VZRVVped'}
    
    # {'ResponseMetadata': {'RequestId': '71dd18f0-898a-4850-ac8c-6592d984036c', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'date': 'Thu, 30 Apr 2020 04:10:45 GMT', 'x-amzn-requestid': '71dd18f0-898a-4850-ac8c-6592d984036c', 'content-length': '300', 'connection': 'keep-alive'}, 'RetryAttempts': 0}, 'message': 'Sorry, can you please repeat that?', 'messageFormat': 'PlainText', 'dialogState': 'ElicitIntent', 'sessionId': '2020-04-30T04:10:45.920Z-MwFPKzTj'}

    # if 'slots' not in response:
    #     return {'status': False,
    #             'message': []
    #             }
    slots = []            
    for key, val in response['sessionState']['intent']['slots'].items():
        if val != None:
            slots.append(val['value']['originalValue'])
    
    print("slots: ", slots)

    photos = es_search_photo_by_label([slot for slot in slots if slot])
    print(photos)
    photo_urls = []
    for photo in photos:
        temp=photo['objectKey']
        photo_url = 'https://photos-album-6998.s3.amazonaws.com/' + temp
        if photo_url not in photo_urls:
            photo_urls.append(photo_url)
    return {
        'status': True,
        'message': photo_urls
    }
    
    

# # Define the client to interact with Lex
# client = boto3.client('lexv2-runtime')
# def lambda_handler(event, context):
#     print(event)
#     print(context)
#     # msg_from_user = event['messages'][0]['unstructured']['text']
#     # print(msg_from_user)

#     response = client.recognize_text(
#             botId='THGAWADSYH', # MODIFY HERE
#             botAliasId='H6XM2RZQ5G', # MODIFY HERE
#             localeId='en_US',
#             sessionId='testuser3',
#             text="Show me pictures of ")
    
#     # response = client.post_text(
#     #         botName='DiningConciergeV2', # MODIFY HERE
#     #         botAliasId='RDOJLLYT8V', # MODIFY HERE
#     #         userId=user_id,
#     #         inputText="hello"
#     #         )
#     print("Response", response)
    
#     intent = response.get('sessionState')
#     intent = intent.get('intent').get('name')
#     print("Intent: ",intent)
    
#     msg_from_lex = response.get('messages', [])
#     print(msg_from_lex)
#     if msg_from_lex:
#         resp = {}
#         if(True):
#         #if(intent == "GreetingIntent"):
#             print("Here")
#             resp = {
#                 'statusCode': 200,
#                 'messages': [{"type": "unstructured", "unstructured":{"text":msg_from_lex[0]['content']}}],
#                 "headers": { 
#                 "Access-Control-Allow-Origin": "*" 
#                 }  
#             }
       
#         return resp
    
