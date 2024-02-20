from flask import Flask, jsonify, request, redirect
app = Flask(__name__)

@app.route('/convert',methods=['POST'])
def convert():
    req = request.json
    data = {
        'title': 'Process music',
        'message': ''
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5003,debug=True)


