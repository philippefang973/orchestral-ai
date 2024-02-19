from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/signin',methods=['POST'])
def get_data():
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
def get_data():
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