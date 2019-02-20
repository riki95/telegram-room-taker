import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = 'uc_rooms'


def query(occupied):
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression=Key('occupied').eq(occupied)
    )

    items = response['Items']

    return sorted(items, key=lambda r: r['room'])


def scan():
    table = dynamodb.Table(table_name)

    response = table.scan()

    items = response['Items']

    return sorted(items, key=lambda r: r['room'])


def insert(room, occupied):
    table = dynamodb.Table(table_name)

    item = {
        'room': room,
        'occupied': occupied
    }

    table.put_item(Item=item)


def update(room, occupied):
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={'room': room},
        UpdateExpression='set occupied = :o',
        ExpressionAttributeValues={
            ':o': occupied
        }
    )

