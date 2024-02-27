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

@app.route('/signin',methods=['POST'])
def signin():
    req = request.json
    #Show form
    if not req :
        data = {
            'title': 'Sign In',
            'message': 'form'
        }
        return jsonify(data)
    #Form validation
    else :
        return jsonify({})
    
@app.route('/signup',methods=['POST'])
def signup():
    req = request.json
    #Show form
    if not req :
        data = {
            'title': 'Sign Up',
            'message': 'form'
        }
        return jsonify(data)
    #Form validation
    else :
        return jsonify({})
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)