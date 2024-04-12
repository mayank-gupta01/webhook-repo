from flask import Blueprint, json, jsonify, request
# from app.extensions import mongo
from app.extensions import git_db
from datetime import datetime, timezone, timedelta
import pymongo
webhook = Blueprint('Webhook', __name__)

@webhook.route('/')
def hello():
    return 'welcome', 200

# we need to make a receiver for push 
@webhook.route('/push', methods=["POST"])
def push():
    try:
        json_data = request.json
        print(json.dumps(request.json))
        request_id = json_data.get('after')
        author = json_data.get('commits', [{}])[0].get('author', {}).get('username')
        to_branch = json_data.get('ref', '').split("/")[-1]
        timestamp = json_data.get('commits', [{}])[0].get('timestamp').split("+")[0]

        # Insert data into MongoDB
        if request_id and author and to_branch and timestamp:
            print('its pushing time -------------------')
            git_db.insert_one({
                "request_id": request_id,
                "author": author,
                "action":"PUSH",
                "to_branch": to_branch,
                "timestamp": timestamp
            })
            return jsonify({"message": "Push request data inserted successfully"}), 200
        else:
            return jsonify({"error": "Invalid payload format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# we need to make a request for pull request
@webhook.route('/pr', methods=["POST"])
def pr():
    try:
        print("This is a pull request to github repo--------------------->>>>>>>>>>>>>>>")
        json_data = request.json
        if(json_data['action'] == "opened"):
            author = json_data['pull_request']['base']['user']['login']
            from_branch = json_data['pull_request']['head']['ref']
            to_branch = json_data['pull_request']['base']['ref']
            timestamp = json_data['pull_request']['created_at']

            print(author, from_branch, to_branch, timestamp)
            # Insert data into MongoDB
            if author and to_branch and from_branch and timestamp:
                print('its time to create document -------------------')
                git_db.insert_one({
                    "author": author,
                    "action":"PULL_REQUEST",
                    "from_branch":from_branch,
                    "to_branch": to_branch,
                    "timestamp": timestamp
                })
        return jsonify({"message": "Pull request data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@webhook.route('/get-all-data')
def getAllData():
    try:
        print('this is route for getting all data ------------------')
        cursor = git_db.find().sort("timestamp", pymongo.DESCENDING)
        data = [{**document, "_id": str(document["_id"])} for document in cursor]
        if len(data)>8:
            data = data[:8]
        # print(data)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500