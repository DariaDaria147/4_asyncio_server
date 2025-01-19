# ИСАДИЧЕВА ДАРЬЯ, ДПИ22-1

import asyncio

# Конфигурация сервера: IP-адрес и порт для подключения клиентов
SERVER_HOST = 'localhost'  # Локальный адрес сервера
SERVER_PORT = 9095         # Порт, на котором будет работать сервер

# Асинхронная функция для обработки подключения клиента
async def handle_client(client_reader, client_writer):
    """
    Обрабатывает подключение клиента: принимает данные, отправляет их обратно и закрывает соединение.
    
    :param client_reader: Асинхронный поток для чтения данных от клиента
    :param client_writer: Асинхронный поток для отправки данных клиенту
    """
    # Читаем данные, переданные клиентом (максимальный размер — 100 байт)
    client_data = await client_reader.read(100)
    client_message = client_data.decode()  # Преобразуем байты в строку
    client_address = client_writer.get_extra_info('peername')  # Получаем IP и порт клиента

    # Выводим полученное сообщение и адрес клиента
    print(f"Получено сообщение: {client_message!r} от клиента: {client_address!r}")

    # Отправляем сообщение обратно клиенту (реализуем эхо-сервер)
    print(f"Отправляем обратно: {client_message!r}")
    client_writer.write(client_data)  # Записываем данные в поток отправки
    await client_writer.drain()       # Убеждаемся, что данные отправлены полностью

    # Закрываем соединение с клиентом
    print(f"Закрываем соединение с клиентом: {client_address!r}")
    client_writer.close()
    await client_writer.wait_closed()  # Ждем полного закрытия соединения

# Асинхронная функция для запуска сервера
async def start_server():
    """
    Запускает сервер и обрабатывает подключения клиентов.
    """
    # Создаем сервер с обработчиком подключения handle_client
    server = await asyncio.start_server(handle_client, SERVER_HOST, SERVER_PORT)

    # Получаем информацию об адресе и порте сервера
    server_address = server.sockets[0].getsockname()
    print(f"Сервер запущен и доступен по адресу: {server_address}")

    # Контекстный менеджер для запуска сервера и ожидания новых подключений
    async with server:
        await server.serve_forever()

# Запуск основного события (цикла обработки)
asyncio.run(start_server())
