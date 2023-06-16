import grpc

import chat_pb2
import chat_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    
    initial_message = chat_pb2.Message()
    initial_message.sender = "Kevin"
    print("Ketikkan Pesan: ")
    initial_message.content = input()

    responses = stub.SendMessage(iter([initial_message]))
    for response in responses:
        print(f"{response.content}")

if __name__ == '__main__':
    run()
