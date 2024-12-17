import socket

# Создаем TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET указывает на использование IPv4, а SOCK_STREAM на TCP

# привязка сокета к адесу и порту
server_address = ('localhost', 12345)  # используем localhost и порт 12345
server_socket.bind(server_address)

# устанавлваем режим ожидания подключения
server_socket.listen(1) # для одного клиента
print("Сервер запущен и ожидает подключения на порту 12345...")

# принятие подключение от клиента
client_socket, client_address = server_socket.accept()
print(f"Подключение установлено с {client_address}")

# идет получение сообщения от клиента
data = client_socket.recv(1024)  # устанавливаем максимальный размер получаемых данных 1024 байта
print(f"Получено сообщение от клиента: {data.decode('utf-8')}")

# тут идет обратное сообщение клинету
client_socket.sendall(data)

# закрытие соединения
client_socket.close() 
server_socket.close() 
print("Соединение закрыто.")