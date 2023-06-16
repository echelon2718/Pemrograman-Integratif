import os
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

clients = []

@app.route('/')
def index():
    return open(os.path.join(os.path.dirname(__file__), 'index.html')).read()

@app.route('/stream')
def stream():
    def event_stream():
        clients.append(response)
        yield 'data: {"message": "Connected"}\n\n'

        while True:
            message = yield
            response = 'data: {"message": "' + message + '"}\n\n'
            yield response

    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/send', methods=['POST'])
def send():
    message = request.json['message']
    for client in clients:
        client.send(message)

    return jsonify({'success': True, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)