import socket  
import threading  
import time  
from flask import Flask, jsonify  

app = Flask(__name__)  
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

@app.route('/clients', methods=['GET'])  
def get_connected_clients():  
    """Возвращает список всех подключенных клиентов в формате JSON."""  
    return jsonify(clients)  

def print_connected_clients():  
    """Выводит список всех подключенных клиентов."""  
    while True:  
        if clients:  
            print("\nConnected clients:")  
            for client in clients:  
                print(f"Domain/Computer: {client[0]}, IP: {client[1]}")  
        else:  
            print("\nNo connected clients.")  
        time.sleep(10)  # Обновление каждые 10 секунд  

if __name__ == "__main__":  
    server_thread = threading.Thread(target=start_server)  
    server_thread.start()  

    # Запускаем Flask сервер на другом потоке  
    app.run(port=8888)  # Замените на нужный порт для Flask  
    print_connected_clients()  # Запускаем вывод списка клиентов