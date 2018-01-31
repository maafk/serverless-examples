import boto3
import os
import uuid
from chalice import Chalice
from chalice import BadRequestError, NotFoundError

app = Chalice(app_name='dad-jokes')
app.debug = True
client = boto3.client('dynamodb')


@app.route('/', cors=True)
def index():
    response = client.scan(
        TableName=os.environ['APP_TABLE_NAME'],
        Limit=10
    )

    return response


@app.route('/joke', methods=['POST'])
def add_joke():
    joke = app.current_request.json_body.get('joke', '')
    punchline = app.current_request.json_body.get('punchline', '')

    if not joke or not punchline:
        raise BadRequestError(
            "You must provide an object with keys of 'joke' and 'punchline'")
    joke_uuid = str(uuid.uuid4())
    response = client.put_item(
        TableName=os.environ['APP_TABLE_NAME'],
        Item={
            'uuid': {'S': joke_uuid},
            'votes': {'N': '0'},
            'joke': {'S': joke},
            'punchline': {'S': punchline}
        }
    )
    print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {"joke_uuid": joke_uuid}
    else:
        raise BadRequestError("Error writing to table")


@app.route('/joke/{joke_uuid}', methods=['GET'])
def get_joke(joke_uuid):
    try:
        response = client.get_item(
            TableName=os.environ['APP_TABLE_NAME'],
            Key={
                'uuid': {'S': joke_uuid}
            }
        )
    except Exception as e:
        raise NotFoundError(joke_uuid)

    return response


@app.route('/joke/{joke_uuid}', methods=['PUT'], cors=True)
def vote_on_joke(joke_uuid):
    vote_type = app.current_request.json_body.get('vote', 0)
    if not vote_type or vote_type not in ['up', 'down']:
        raise BadRequestError(
            "Please provide 'up' or 'down' in your request body")

    if vote_type == 'up':
        UpdateExpression = 'SET votes = votes + :n'
    else:
        UpdateExpression = 'SET votes = votes - :n'
    try:
        response = client.update_item(
            TableName=os.environ['APP_TABLE_NAME'],
            Key={
                'uuid': {'S': joke_uuid}
            },
            UpdateExpression=UpdateExpression,
            ExpressionAttributeValues={
                ":n": {"N": "1"}
            }
        )
    except Exception as e:
        raise NotFoundError(e)

    return response


@app.route('/joke/{joke_uuid}', methods=['DELETE'])
def delete_joke(joke_uuid):
    response = client.delete_item(
        TableName=os.environ['APP_TABLE_NAME'],
        Key={
            'uuid': {'S': joke_uuid}
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {"success": "Deleted {}".format(joke_uuid)}
    else:
        raise BadRequestError("Error writing to table")
