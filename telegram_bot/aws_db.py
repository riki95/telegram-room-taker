import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = 'uc_rooms'


def query(occupied, chat_id):
    table = dynamodb.Table(table_name)

    response = ''
    if chat_id != '0':
        response = table.scan(  # Return all of the rooms occupied by a certain chat_id
            FilterExpression=Key('occupied').eq(occupied) and Key('id').eq(chat_id)
        )
    else:
        response = table.scan(  # Otherwise just return all of the free rooms
            FilterExpression=Key('occupied').eq(occupied),
        )

    items = response['Items']

    return sorted(items, key=lambda r: r['room'])


def scan():
    table = dynamodb.Table(table_name)

    response = table.scan()

    items = response['Items']

    return sorted(items, key=lambda r: r['room'])


def insert(room, occupied, chat_id):
    table = dynamodb.Table(table_name)

    item = {
        'room': room,
        'occupied': occupied,
        'id': chat_id
    }

    table.put_item(Item=item)


def update(room, occupied, chat_id):
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={'room': room},
        UpdateExpression='set occupied = :o, id=:id',
        ExpressionAttributeValues={
            ':o': occupied,
            ':id': chat_id
        }
    )

