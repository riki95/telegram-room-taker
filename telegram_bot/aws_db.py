import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = 'uc_rooms'


def query(occupied):
    table = dynamodb.Table(table_name)

    items = table.scan(
        FilterExpression=Key('occupied').eq(True)
    )

    return items


def scan():
    table = dynamodb.Table(table_name)

    items = table.scan()
    return items['Items']


def insert(room, occupied):
    table = dynamodb.Table(table_name)

    item = {
        'room': room,
        'occupied': occupied
    }

    table.put_item(Item=item)

def update(room, occupied):
    table = dynamodb.Table(table_name)

    response = table.update_item(
        Key={'room': room},
        UpdateExpression='set occupied = :o',
        ExpressionAttributeValues={
            ':o': occupied
        },
        ReturnValues='UPDATED_NEW'
    )

    return response

