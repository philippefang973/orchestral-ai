from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session

import requests
app = Flask(__name__)
app.secret_key = 'V3RY-S3KR3T-K3Y'
CORS(app, resources={r"/*": {"origins": ["http://angular.default.svc.cluster.local:4200"]}})

@app.route('/',methods=['POST'])
def homepage():
    return "connected" in session
    
@app.route('/disconnect',methods=['POST'])
def disconnect():
    app.logger.info(f"User {session["connected"]} disconnected")
    session.clear()

@app.route('/signin',methods=['POST'])
def signin():
    if "connected" in session :
        return redirect(url_for('dashboard'))
    else :
        response = requests.post("http://auth.default.svc.cluster.local:5001/signin",json=request.get_json()).json()
        if response["msg"]=="success" :
            session["connected"]=request.get_json().get("username")
        return response

@app.route('/signup',methods=['POST'])
def signup():
    if "connected" in session :
        return redirect(url_for('dashboard'))
    else :
        response = requests.post("http://auth.default.svc.cluster.local:5001/signup",json=request.get_json()).json()
        if response["msg"]=="success" :
            session["connected"]=request.get_json().get("username")
        return response

@app.route('/dashboard',methods=['POST'])
def dashboard():
    if "connected" in session :
        return requests.post("http://dashboard.default.svc.cluster.local:5002/dashboard",json={"username":session["connected"]}).json()
    return jsonify({})

@app.route('/convert',methods=['POST'])
def convert():
    if "connected" in session :
        return requests.post("http://converter.default.svc.cluster.local:5003/convert",json={"username":session["connected"]}).json()
    return jsonify({})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
