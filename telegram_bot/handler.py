import json
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

#########################################################
import boto3
dynamodb = boto3.resource('dynamodb')


def scan_table(table_name):
    table = dynamodb.Table(table_name)
    
    items = table.scan()
    return items['Items']


def insert_table(table_name, room, status):
    table = dynamodb.Table(table_name)
    
    item = {
        'room': room,
        'status': status
    }
    
    table.put_item(Item=item)


def format_items(items):
    res = ''
    
    for item in items:
        res += json.dumps(item) + '\n'
        
    return res


def handler(event, context):
    print('=== start ===')
    
    #print(scan_table('uc_db'))
    #insert_table('uc_db', 'r4', 'ok')
    #print(scan_table('uc_db'))
    
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]

        if '/scan' in message:
            response = format_items(scan_table('uc_db'))
        elif '/add' in message:
            mess_args = message.split()
            r = mess_args [1]
            response = r
        else:
            response = 'hello' #json.dumps(event)

        print('res', response)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print('exception', e)
    
    print('=== end ===')
    return {"statusCode": 200, "body": 'aa'}

