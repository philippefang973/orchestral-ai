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