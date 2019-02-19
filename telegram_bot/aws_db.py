import json
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'uc_rooms'


def scan_table():
    table = dynamodb.Table(table_name)
    
    items = table.scan()
    return items['Items']


def insert_table(room, status):
    table = dynamodb.Table(table_name)

    item = {
        'room': room,
        'occupied': status
    }

    table.put_item(Item=item)
