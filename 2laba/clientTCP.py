import socket

# TCP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Вот тут идет подключение к сокету
server_address = ('localhost', 12345)  # адрес и порт сервера
client_socket.connect(server_address)
print("Подключение к серверу установлено.")

# тут отправляется сообщение серверу
message = "Каждая работа выглядит интересной — пока ею не займешься."
client_socket.sendall(message.encode('utf-8'))
print(f"Отправлено сообщение: {message}")

# идет получение сообщения от сервера 
data = client_socket.recv(1024)
print(f"Получено сообщение от сервера: {data.decode('utf-8')}")

# закрытие  соединения
client_socket.close()
print("Соединение закрыто.")