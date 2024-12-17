import socket

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# адрес и порт сервера
server_address = ('localhost', 12345)

# отправляем сообщение серверу
message = "— Побудь здесь. Если там неопасно, я свистну. \n — А если опасно? \n — Заору."
client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Отправлено сообщение: {message}")

# Получаем ответ от сервера
data, server = client_socket.recvfrom(1024)
print(f"Получено сообщение от сервера: {data.decode('utf-8')}")

# закрываем сокет
client_socket.close()
print("Соединение закрыто.")