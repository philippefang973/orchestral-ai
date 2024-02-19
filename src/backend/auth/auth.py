from flask import Flask, jsonify, request, redirect
app = Flask(__name__)
@app.route('/',methods=['GET'])
def homepage():
    return redirect('http://localhost:5000/')

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
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)