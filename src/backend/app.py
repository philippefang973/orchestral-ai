from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/',methods=['POST'])
def get_data():
    data = {
        'title': 'Welcome to Orchestral AI',
        'message': 'Homepage'
    }
    return jsonify(data)

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
    
@app.route('/dashboard',methods=['POST'])
def get_data():
    req = request.json
    data = {
        'title': 'Hello',
        'message': 'dashboard'
    }
    return jsonify(data)

@app.route('/infos',methods=['POST'])
def get_data():
    req = request.json
    data = {
        'title': 'Personal information',
        'message': ''
    }
    return jsonify(data)

@app.route('/prediction',methods=['POST'])
def get_data():
    req = request.json
    data = {
        'title': 'Process music',
        'message': ''
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()


