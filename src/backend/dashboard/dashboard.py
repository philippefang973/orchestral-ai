from flask import Flask, jsonify, request, redirect
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