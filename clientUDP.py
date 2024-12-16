import socket

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес и порт сервера
server_address = ('localhost', 12345)

# Отправляем сообщение серверу
message = "Привет, UDP-сервер!"
client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Отправлено сообщение: {message}")

# Получаем ответ от сервера
data, server = client_socket.recvfrom(1024)
print(f"Получено сообщение от сервера: {data.decode('utf-8')}")

# Закрываем сокет
client_socket.close()
print("Соединение закрыто.")