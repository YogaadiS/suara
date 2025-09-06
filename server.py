import socket
import threading

# Fungsi untuk menangani setiap client yang terhubung
def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"[{addr}] {msg}")
            broadcast(msg, client_socket)
        except:
            break
    client_socket.close()
    clients.remove(client_socket)
    print(f"[DISCONNECTED] {addr} disconnected.")

# Fungsi untuk mengirim pesan ke semua client kecuali pengirim
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

print("[STARTED] Server is listening...")

clients = []

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()