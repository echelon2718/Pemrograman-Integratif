import os
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

clients = []

import openai
openai.api_key = "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"

class GPT3:
    def __init__(self):
        self.text = "\nJacob: Halo, saya Jacob!\nHuman:"

    def __chatRes(self, text):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.9,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["Human:", "Jacob:"]
        )
        return response.choices[0].text
    
    def chat(self, text):
        self.text += f"\n{text}\nJacob:"
        resp = self.__chatRes(self.text)
        self.text += f"{resp}\nHuman:"

        return resp
    
gpt3 = GPT3()

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
    response = gpt3.chat(message)  # Use gpt3.chat() to get the response
    for client in clients:
        client.send(response)

    return jsonify({'success': True, 'message': response})

if __name__ == '__main__':
    app.run(debug=True)