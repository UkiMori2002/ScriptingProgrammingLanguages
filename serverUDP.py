import socket

# создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET указывает на использование IPv4, а SOCK_DGRAM на UDP

# Привязываем сокет к адресу и порту
server_address = ('localhost', 12345)  # используем localhost и порт 12345
server_socket.bind(server_address)
print("UDP-сервер запущен и ожидает данных на порту 12345...")

# ожидаем данные от клиента
data, client_address = server_socket.recvfrom(1024)  # тут устанавливаем максимальный размер получаемых данных от клиента -1024 байта
print(f"Получено сообщение от клиента {client_address}: {data.decode('utf-8')}")

# отправляем данные обратно клиенту
server_socket.sendto(data, client_address)
print(f"Отправлено сообщение обратно клиенту {client_address}")

# закрываем сокет
server_socket.close()
print("Сервер завершил работу.")