import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_address = ('localhost', 12345)  # Используем localhost и порт 12345
server_socket.bind(server_address)
print("UDP-сервер запущен и ожидает данных на порту 12345...")

while True:
    # Ожидаем данные от клиента
    data, client_address = server_socket.recvfrom(1024)  # Максимальный размер данных 1024 байта
    print(f"Получено сообщение от клиента {client_address}: {data.decode('utf-8')}")

    # Отправляем данные обратно клиенту
    server_socket.sendto(data, client_address)
    print(f"Отправлено сообщение обратно клиенту {client_address}")

    # Закрываем сокет (если нужно завершить работу сервера)
    # server_socket.close()
    # break