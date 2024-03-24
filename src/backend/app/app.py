import sys
from flask import Flask, jsonify, request, session, redirect, url_for, send_file
from flask_cors import CORS
from flask_session import Session
from zipfile import ZipFile
import io
import requests

host,auth_service_ip,converter_service_ip = "","",""
try :
    if sys.argv[1]=="local" :
        host = "127.0.0.1"
        auth_service_ip = "http://localhost:5001"
        converter_service_ip = "http://localhost:5003"
    if sys.argv[1]=="deploy" :
        host = "0.0.0.0"
        auth_service_ip = "http://auth.default.svc.cluster.local:5001"
        converter_service_ip = "http://converter.default.svc.cluster.local:5003"
except Exception as e : print(e)

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
    session.clear()
    #session.pop('connected', None)
    #session.pop('history', None)
    session.modified = True
    return jsonify({})

@app.route('/signin',methods=['POST'])
def signin():
    global auth_service_ip
    if "connected" in session :
        return dashboard()
    else :
        response = requests.post(auth_service_ip+"/signin",json=request.get_json()).json()
        if response.get('msg')=='success' :
            session['connected']=request.get_json().get("username")
            session.modified = True
        return response

@app.route('/history',methods=['POST'])
def history() :
    global auth_service_ip
    if "connected" in session :
        if "history" in session :
            return jsonify({"history":session.get("history")})
        else :
            response = requests.post(auth_service_ip+"/history",json={"username":session.get('connected')}).json()
            if "history" in response :
                session['history']=response.get("history")
                session.modified = True
            return response 
    return jsonify({})


@app.route('/signup',methods=['POST'])
def signup():
    global auth_service_ip
    if "connected" in session :
        return dashboard()
    else :
        response = requests.post(auth_service_ip+"/signup",json=request.get_json()).json()
        if response.get('msg')=='success' :
            session['connected']=request.get_json().get("username")
            session['history']=request.get_json().get("history")
            session.modified = True
        return response

@app.route('/dashboard',methods=['POST'])
def dashboard():
    if "connected" in session :
        return jsonify({"msg":"success","userdata":{"username": session.get("connected"),"history":session.get("history")}})
    else : 
        return jsonify({"msg":"failed"})

@app.route('/convert',methods=['POST'])
def convert():
    global converter_service_ip
    if "connected" in session :
        multipart_form_data = {
            'audio': (request.files['audio'].filename, request.files['audio'], request.files['audio'].mimetype)
        }
        response = requests.post(converter_service_ip+"/convert",
            files=multipart_form_data,data={"username":session.get('connected')}).json()
        if "conversion" in response : 
            if session["history"] : 
                session['history']+=[(request.files['audio'].filename,response.get("conversion"))]
            else : 
                session["history"]=[(request.files['audio'].filename,response.get("conversion"))]
            session.modified = True
        return response
    return jsonify({})

if __name__ == '__main__':
    app.run(host=host,port=5000,debug=True)
