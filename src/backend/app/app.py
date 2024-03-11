from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session

import requests
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:4200","http://angular.default.svc.cluster.local:4200"]}})
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_COOKIE_SECURE"]=True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/',methods=['POST'])
def homepage():
    if "connected" in session : return jsonify({"msg":"connected"})
    return jsonify({"msg":"not connected"})
    
@app.route('/disconnect',methods=['POST'])
def disconnect():
    app.logger.info(f"User {session.get('connected')} disconnected")
    session.pop('connected', None)
    session.modified = True
    return jsonify({})

@app.route('/signin',methods=['POST'])
def signin():
    if "connected" in session :
        return dashboard()
    else :
        response = requests.post("http://auth.default.svc.cluster.local:5001/signin",json=request.get_json()).json()
        if response["msg"]=="success" :
            session['connected']=request.get_json().get("username")
            session.modified = True
        return response

@app.route('/signup',methods=['POST'])
def signup():
    if "connected" in session :
        return dashboard()
    else :
        response = requests.post("http://auth.default.svc.cluster.local:5001/signup",json=request.get_json()).json()
        if response["msg"]=="success" :
            session['connected']=request.get_json().get("username")
            session.modified = True
    
        return response

@app.route('/dashboard',methods=['POST'])
def dashboard():
    if "connected" in session :
        return requests.post("http://dashboard.default.svc.cluster.local:5002/dashboard",json={"username":session.get('connected')}).json()
    return jsonify({})

@app.route('/convert',methods=['POST'])
def convert():
    if "connected" in session :
        return requests.post("http://converter.default.svc.cluster.local:5003/convert",json={"username":session.get('connected')}).json()
    return jsonify({})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
