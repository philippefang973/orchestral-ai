from flask import Flask, jsonify, request, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://philippefang973:tpalt2023@orchestralai-db.roc0uk6.mongodb.net/?retryWrites=true&w=majority"
mongodb = MongoClient(uri, server_api=ServerApi('1'))
try:
    mongodb.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)
@app.route('/dashboard',methods=['POST'])
def dashboard():
    req = request.json
    data = {
        'title': 'Hello',
        'message': 'dashboard'
    }
    return jsonify(data)

@app.route('/infos',methods=['POST'])
def infos():
    req = request.json
    data = {
        'title': 'Personal information',
        'message': ''
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5002,debug=True)