from flask import Flask, jsonify
import requests
app = Flask(__name__)
@app.route('/',methods=['GET'])
def homepage():
    data = {
        'title': 'Welcome to Orchestral AI',
        'message': 'Homepage'
    }
    return jsonify(data)

@app.route('/signin',methods=['GET'])
def signin():
    response = requests.post("http://auth.default.svc.cluster.local:5001/signin",json={})
    return response.json()

@app.route('/signup',methods=['GET'])
def signup():
    response = requests.post("http://auth.default.svc.cluster.local:5001/signup",json={})
    return response.json()

@app.route('/dashboard',methods=['GET'])
def dashboard():
    response = requests.post("http://dashboard.default.svc.cluster.local:5002/dashboard",json={})
    return response.json()

@app.route('/infos',methods=['GET'])
def infos():
    response = requests.post("http://dashboard.default.svc.cluster.local:5002/infos",json={})
    return response.json()

@app.route('/convert',methods=['GET'])
def convert():
    response = requests.post("http://converter.default.svc.cluster.local:5003/convert",json={})
    return response.json()


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
