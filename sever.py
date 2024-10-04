import socket, sys
from _thread import *

def thread_client(conn, addr):
    print(f"Connected with {addr}, starting the game...")

    reply = ""
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                break
            reply = data.decode("utf-8")
            print(f"Received from {addr}: {reply})")
            conn.sendall(reply.encode("utf-8"))
        except:
            print(f"Error occurred while receiving data from client {addr}")
            break


def start_sever():
    sever = "192.168.1.15"
    port = 5555
    hostname = socket.gethostname()

    sever = socket.gethostbyname(hostname)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((sever, port))
        s.listen(5)
        print(f"Server is listening on {sever}:{port}")
    except socket.error as e:
        print(f"Server could not bind to the address: {e}")
        exit()
    
    print("Waiting for client...")
    while True:
        conn, addr = s.accept()
    
        print(f"Connected with {addr}")
        start_new_thread(thread_client, (conn, addr))

start_sever()