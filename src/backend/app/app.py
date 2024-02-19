from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/',methods=['POST'])
def get_data():
    data = {
        'title': 'Welcome to Orchestral AI',
        'message': 'Homepage'
    }
    return jsonify(data)


