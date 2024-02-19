from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/convert',methods=['POST'])
def get_data():
    req = request.json
    data = {
        'title': 'Process music',
        'message': ''
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()


