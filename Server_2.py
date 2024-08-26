import socket  
import time  
import threading  
import json  # Импортируем модуль для работы с JSON  

clients = []  

def handle_client(client_socket, address):  
    """Обрабатывает подключение клиента."""  
    print(f"Client connected: {address}")  
    clients.append(address)  # Добавляем клиента в список  

    while True:  
        try:  
            data = client_socket.recv(1024).decode()  
            if not data:  
                break  
            print(f"Received data from {address}: {data}")  
        except Exception as e:  
            print(f"Error: {e}")  
            break  

    print(f"Client disconnected: {address}")  
    clients.remove(address)  # Удаляем клиента из списка  
    client_socket.close()  

def start_server():  
    """Запускает сервер."""  
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server.bind(("localhost", 8888))  # Замените на нужный адрес и порт  
    server.listen(5)  
    print("Server started, waiting for connections...")  

    while True:  
        client_socket, address = server.accept()  
        threading.Thread(target=handle_client, args=(client_socket, address)).start()  

def get_connected_clients():  
    """Возвращает список всех подключенных клиентов в формате JSON."""  
    return json.dumps([{"domain": client[0], "ip": client[1]} for client in clients])  

def handle_request(client_socket):  
    """Обрабатывает запросы от клиентов."""  
    request = client_socket.recv(1024).decode()  
    if request.startswith("GET /clients"):  
        response = get_connected_clients()  
        client_socket.send(response.encode())  
    client_socket.close()  

def start_http_server():  
    """Запускает HTTP-сервер для обработки запросов."""  
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    http_server.bind(("localhost", 8888))  # Замените на нужный адрес и порт  
    http_server.listen(5)  
    print("HTTP server started, waiting for requests...")  

    while True:  
        client_socket, address = http_server.accept()  
        threading.Thread(target=handle_request, args=(client_socket,)).start()  

if __name__ == "__main__":  
    server_thread = threading.Thread(target=start_server)  
    server_thread.start()  

    http_thread = threading.Thread(target=start_http_server)  
    http_thread.start()