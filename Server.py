import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8888))
server_socket.listen()

connected_clients = {}

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    data = client_socket.recv(1024).decode()

    if data.startswith("ACTIVITY"):
        parts = data.split("|")
        client_name = parts[1]
        ip_address = parts[2]
        activity_time = parts[3]
        connected_clients[client_name] = (ip_address, activity_time)
        client_socket.send("Activity data received".encode())
    else:
        # Логика для сохранения скриншота на сервере
        with open(f"screenshot_{time.time()}.jpg", 'wb') as file:
            file.write(data)
        client_socket.send("Screenshot received".encode())

    client_socket.close()
