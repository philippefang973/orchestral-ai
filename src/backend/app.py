from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def get_data():
    data = {
        'title': 'Welcome to Angular-Python App',
        'message': 'This is an example integration between Angular and Python!'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()


