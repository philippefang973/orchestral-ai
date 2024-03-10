from flask import Flask, jsonify, request, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://philippefang973:tpalt2023@orchestralai-db.roc0uk6.mongodb.net/?retryWrites=true&w=majority&appName=OrchestralAI-DB"
mongodb = MongoClient(uri, server_api=ServerApi('1'))
collection = None
try:
    mongodb.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    collection = mongodb["default"]["users"]
except Exception as e:
    print(e)

app = Flask(__name__)
@app.route('/dashboard',methods=['POST'])
def dashboard():
    global collection
    req = request.get_json()
    query = {"username": req.get("username")}
    result = collection.find_one(query)
    data = {"msg":"failed"}
    # Check if username exists
    if result :
        data = {"msg":"success","userdata":result}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5002,debug=True)