"""Unit-tests for utils"""

import sys
import unittest
import json
sys.path.append('D:\\клиент-серверные приложения\\Lesson_3_Sidorova\\client-server-application')
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.utils import get_message, send_message


class SocketTest:
    """ Тестовый класс, на основе которого будут проходить все тесты"""
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, mes_to_send):
        """Функция отправки сообщений"""
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # сохраняем, что должно быть отправлено в сокет
        self.receved_message = mes_to_send

    def recv(self, max_len):
        """Функция получения сообщений (из сокета)"""
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestClass(unittest.TestCase):
    """Класс, выполняющий тестирование"""
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'root'}
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_mes(self):
        """ Функция отправки сообщения"""
        socket_test = SocketTest(self.test_dict_send)
        send_message(socket_test, self.test_dict_send)
        self.assertEqual(socket_test.encoded_message, socket_test.receved_message)
        with self.assertRaises(Exception):
            send_message(socket_test, socket_test)

    def test_get_mes(self):
        """ Функция приема сообщения"""
        test_socket_ok = SocketTest(self.test_dict_recv_ok)
        test_socket_error = SocketTest(self.test_dict_recv_err)
        self.assertEqual(get_message(test_socket_ok), self.test_dict_recv_ok)
        self.assertEqual(get_message(test_socket_error), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()


