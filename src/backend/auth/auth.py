from flask import Flask, jsonify, request, redirect, send_file
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_bcrypt import Bcrypt
from gridfs import GridFS
import io
import sys
import base64

uri = "mongodb+srv://philippefang973:tpalt2023@orchestralai-db.roc0uk6.mongodb.net/?retryWrites=true&w=majority&appName=OrchestralAI-DB"
mongodb = MongoClient(uri, server_api=ServerApi('1'))
fs, collection, host = None, None, ""
try:
    mongodb.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    fs = GridFS(mongodb["default"])
    collection = mongodb["default"]["users"]
    host = "0.0.0.0" if sys.argv[1]=="deploy" else "127.0.0.1"
except Exception as e:
    print(e)

app = Flask(__name__)
bcrypt = Bcrypt(app)


# Sign in 
@app.route('/signin',methods=['POST'])
def signin():
    global collection
    req = request.get_json()
    username, pwd = req.get("username"), req.get("password")
    query = {"username": username}
    result = collection.find_one(query)
    data = {}
    # Check if username exists
    if result :
        if bcrypt.check_password_hash(result.get("password"),pwd) :
            app.logger.info(f"User {username} connect succesfully")
            data = {"msg":"success"}
        else :
            data = {"msg":"Unknown username or password"}
    else :
        data = {"msg":"Unknown username or password"}
    return jsonify(data)
 
@app.route('/history',methods=['POST'])   
def history() :
    global collection, fs
    req = request.get_json()
    username = req.get("username")
    query = {"username": username}
    result = collection.find_one(query)
    if result :
        history = result.get("history")
        files= []
        for r in history :
            file_data = fs.get(r[0])
            serialized_data = base64.b64encode(file_data.read()).decode('utf-8')
            files+=[(r[1],serialized_data)]
        return jsonify({"history":files})
    return jsonify({})


# Sign Up
@app.route('/signup',methods=['POST'])
def signup():
    global collection
    req = request.get_json()
    username, pwd = req.get("username"), req.get("password")
    data = {}
    query = {"username": username}
    result = collection.find_one(query)
    # Check if username is new
    if not result :
        hashed_password = bcrypt.generate_password_hash(pwd).decode('utf-8')
        user_document = {"username": username, "password": hashed_password,"history": []}
        try :
            insert_result = collection.insert_one(user_document)
            app.logger.info(f"User {username} created {insert_result.inserted_id}")
            data = {"msg":"success","username": username,"history":[]}
        except Exception as e:
            app.logger.info(e)
            app.logger.info(f"Error creating new user {username}")
    else :
        data = {"msg":"Username already exists"}
    return jsonify(data)
    
if __name__ == '__main__':
    app.run(host=host,port=5001,debug=True)