from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        # Get the JSON data from the request
        print("RECEIVED REQUEST")
        data = request.get_json()

        # Get the username and cookie from the data
        username = data.get('username')
        cookie = data.get('cookie')

        print(f"Received data from {username} with cookie: {cookie}")

        js_code = 'alert("Hello");'
        response = make_response(js_code)
        response.headers['Content-Type'] = 'application/javascript'
    
        return response
    
    if request.method == 'GET':
        return "It's all good man", 200
    
    else:
        return 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
