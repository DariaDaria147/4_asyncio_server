# ИСАДИЧЕВА ДАРЬЯ, ДПИ22-1

import asyncio

# Конфигурация клиента: адрес сервера и порт для подключения
SERVER_HOST = 'localhost'  # IP-адрес сервера, к которому подключается клиент
SERVER_PORT = 9095         # Порт, на котором ожидает подключения сервер


# Асинхронная функция для клиентской логики
async def send_message_to_server(client_message):
    """
    Устанавливает соединение с сервером, отправляет сообщение и обрабатывает ответ.
    
    :param client_message: Строка, которую клиент отправляет серверу
    """
    # Устанавливаем соединение с сервером
    server_reader, server_writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)

    # Отправляем сообщение серверу
    print(f'Отправка сообщения серверу: {client_message!r}')
    server_writer.write(client_message.encode())  # Кодируем строку в байты
    await server_writer.drain()  # Убеждаемся, что данные полностью отправлены

    # Читаем ответ от сервера (не более 100 байт)
    server_response = await server_reader.read(100)
    print(f'Получен ответ от сервера: {server_response.decode()!r}')  # Декодируем байты в строку

    # Закрываем соединение с сервером
    print("Закрываем соединение с сервером.")
    server_writer.close()  # Закрываем поток записи
    await server_writer.wait_closed()  # Ждем полного закрытия соединения


# Асинхронная функция для запуска клиентской части
async def run_client():
    """
    Запускает клиентскую программу и отправляет сообщение серверу.
    """
    await send_message_to_server("Привет, asyncio!")  # Сообщение, которое клиент отправляет серверу


# Запускаем асинхронное выполнение клиентской программы
asyncio.run(run_client())
