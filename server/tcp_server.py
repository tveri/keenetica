import json
import socket
import threading
from typing import Any, Callable

import settings
from logger import logger


class TCPServer:
    """TCP-сервер для обработки запросов с использованием потоков.

    Сервер принимает подключения, обрабатывает входящие JSON-данные через
    пользовательский обработчик и возвращает результат в JSON-формате.

    Attributes:
        host (str): Хост для подключения. По умолчанию из settings.HOST.
        port (int): Порт для подключения. По умолчанию из settings.PORT.
        request_handler (Callable): Обработчик запросов.
        _is_running (bool): Флаг работы сервера.
        _server_thread (threading.Thread): Поток для работы сервера.
        _socket (socket.socket): Сокет сервера.
    """

    def __init__(
        self,
        request_handler: Callable[[socket.socket, Any], Any],
        host: str = settings.HOST,
        port: int = settings.PORT,
    ):
        """Инициализация TCP-сервера.

        Args:
            request_handler: Функция для обработки запросов. Должна принимать:
                - conn (socket.socket): клиентский сокет
                - data (Any): распарсенные JSON-данные
                Возвращает результат для отправки клиенту.
            host: Хост сервера. По умолчанию из settings.HOST.
            port: Порт сервера. По умолчанию из settings.PORT.
        """
        self.host = host
        self.port = port
        self.request_handler = request_handler
        self._is_running = False
        self._server_thread = None
        self._socket = None

    def _handle_client(self, conn: socket.socket):
        """Обработка подключения клиента.

        Args:
            conn: Клиентский сокет.
        """
        try:
            raw_data = conn.recv(1024**3)  # 1GB
            logger.debug(f"recieved packet: {len(raw_data)}")
            data = json.loads(raw_data)
            result = self.request_handler(conn, data)
            conn.send(json.dumps(result).encode())
            logger.debug("packet processed")
        except Exception as e:
            logger.error(f"packet processing error: {e}")
        finally:
            conn.close()

    def start(self):
        """Запуск сервера в фоновом потоке"""
        logger.info(f"starting server on {self.host}:{self.port}")
        self._is_running = True
        self._server_thread = threading.Thread(target=self._run)
        self._server_thread.start()

    def _run(self):
        """Основной цикл обработки подключений"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self.host, self.port))
        self._socket.listen()
        logger.info("server started")
        try:
            while self._is_running:
                try:
                    conn, addr = self._socket.accept()
                    logger.info(f"client connected: {addr}")
                    threading.Thread(
                        target=self._handle_client, args=(conn,), daemon=True
                    ).start()
                except OSError as e:
                    if not self._is_running:
                        break
                    logger.error(f"error accepting connection: {e}")
        finally:
            self._socket.close()
            logger.debug("server socket closed")

    def stop(self):
        """Остановка сервера.
        Блокирует выполнение до завершения серверного потока.
        """
        self._is_running = False
        if self._socket:
            self._socket.close()
        if self._server_thread:
            self._server_thread.join()
        logger.info("server stopped gracefully")
