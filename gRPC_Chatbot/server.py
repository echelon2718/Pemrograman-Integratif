import grpc
from concurrent import futures
import time
import chat_pb2
import chat_pb2_grpc
import openai

openai.api_key = "SECRET-API-KEY"


def chatRes(text):
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
    return response

class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request_iterator, context):
        for message in request_iterator:
            # Print the received message
            print(f"Received message from {message.sender}: {message.content}")
            greet = "Halo, saya Jacob!"
            text = f"\Jacob:{greet}\nHuman:"
            text = text + f"{message.content}\Jacob:"
            resp = chatRes(text).choices[0].text
            response = chat_pb2.Message()
            response.sender = "Bot"
            response.content = f"{resp}"
            text = text + f"{resp}\nHuman:"
            yield response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started.")
    try:
        while True:
            time.sleep(86000)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
