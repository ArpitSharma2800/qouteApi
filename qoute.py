from flask import Flask
from flask_json_schema import JsonSchema, JsonValidationError
from flask_pymongo import PyMongo
from pymongo import MongoClient, UpdateOne
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import os
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
schema = JsonSchema(app)
client = MongoClient(
    "MONGOURI")

qoute_schema = {
    'uuid': {'type': "string"},
    'properties': {
        "qoute": {
            "type": "array",
            "items":  {
                "type": "object",
                "properties": {
                    "title": {'type': "string"}
                }
            },
        }
    }
}


@app.route('/add', methods=['POST'])
@cross_origin()
@schema.validate(qoute_schema)
def add_user():
    users = client.users.qoute.find_one({'uuid': request.json['uuid']})
    if(users):
        id = request.json['uuid']
        data = request.json['qoute']
        print(data)
        client.users.qoute.update_one(
            {'uuid': id}, {'$addToSet':  {"qoute": data[0]}})
        response = jsonify("User updated successfully")
        response.status_code = 200
        return response
    else:
        print(request.json)
        client.users.qoute.insert(request.json)
        return jsonify({'success': True, 'message': 'qouteList '})


@app.route('/users')
@cross_origin()
def users():
    users = client.users.qoute.find()
    resp = dumps(users)
    return resp


if __name__ == "__main__":
    app.run(debug=True)
