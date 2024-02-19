from flask import Flask, jsonify, request, redirect
app = Flask(__name__)
@app.route('/',methods=['GET'])
def homepage():
    data = {
        'title': 'Welcome to Orchestral AI',
        'message': 'Homepage'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
