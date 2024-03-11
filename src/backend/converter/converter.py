from flask import Flask, jsonify, request, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS
import audio_conversion

uri = "mongodb+srv://philippefang973:tpalt2023@orchestralai-db.roc0uk6.mongodb.net/?retryWrites=true&w=majority&appName=OrchestralAI-DB"
mongodb = MongoClient(uri, server_api=ServerApi('1'))
fs, collection = None, None
try:
    mongodb.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    fs = GridFS(mongodb["default"])
    collection = mongodb["default"]["users"]
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route('/convert',methods=['POST'])
def convert():
    req = request.get_json()
    audio_file = request.files['audio']
    username = req.get("username")
    data = {"msg":"fail"}
    query = {"username": username}
    result = collection.find_one(query)
    if result :
        try : 
            app.logger.info(f"User {username} uploaded: {type(audio_file)}")
            converted_audio = audio_conversion.convert(audio_file)
            file_id = fs.put(audio_file, filename=audio_file.filename, content_type=audio_file.mimetype)
            collection.update_one(query, {"$push": {"history": (file_id,audio_file.filename)}})
            app.logger.info(f"User {username} converted an audio")
            result = collection.find_one(query)
            data = {"msg":"success","history":result.get("history")}
        except Exception :
           app.logger.info(f"Error creating new user {username}")
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5003,debug=True)


