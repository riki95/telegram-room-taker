const AWS = require("aws-sdk");

const docClient = new AWS.DynamoDB.DocumentClient()
const table = "uc_rooms";


exports.handler = function (event, context) {
    console.log('===== start =====')
    
    const body = JSON.parse(event.body);
    const room = body.room;

    query_and_update(room, context);
    
    console.log('===== end =====')
};


function query_and_update(room, context) {
    const params = {
        TableName: table,
        KeyConditionExpression: "room = :r",
        ExpressionAttributeValues: {':r': room}
    };
    
    docClient.query(params, (err, data) => {
        if (err) {
            console.error("Unable to scan the table. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("Scan succeeded.");
            
            const items = data.Items;
            
            if(items.length === 1) {
                update(room, !items[0].occupied, context);
            } else {
                console.error(`query returned ${data.length} values`);
            }
        }
    });
}


function update(room, to_occupy, context) {
    const params = {
        TableName:table,
        Key:{'room': room},
        UpdateExpression: 'set occupied = :o',
        ExpressionAttributeValues:{':o': to_occupy}
    };

    console.log(`Updating room ${room}, to_occupy=${to_occupy}`);

    docClient.update(params, function(err, data) {
        if (err) {
            console.error("Unable to update item. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
            
            const response = {
                statusCode: 200,
                body: to_occupy ? `Room ${room} taken` : `Room ${room} freed`,
            };
            
            context.succeed(response)
        }
    });
}
