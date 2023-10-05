from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key
import uuid

app = Flask(__name__)
CORS(app, resources={r"/todos": {"origins": "http://localhost:3000"}})

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table('sample')

@app.route('/todos', methods=['GET'])
def get_todos():
    response = table.scan()
    return jsonify(response['Items'])

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()

    new_todo = {
    'typeId': str(uuid.uuid4()),
    'text': data['text'], 
    }
    
    table.put_item(Item=new_todo)

    updated_items = table.scan()
    return jsonify(updated_items['Items'])

@app.route('/todos/<string:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    try:
        table.update_item(
            Key={'id': id},
            UpdateExpression='SET text = :text',
            ExpressionAttributeValues={':text': data['text']}
        )
        return jsonify({"message": "Todo updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/todos/<string:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        table.delete_item(Key={'id': id})
        return jsonify({"message": "Todo deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


