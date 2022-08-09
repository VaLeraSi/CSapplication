""" Unit-tests for client """

import sys
sys.path.append('D:\\клиент-серверные приложения\\Lesson_3_Sidorova\\client-server-application')
import unittest
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    """ class with tests"""

    def test_create_presence(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_code_200(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_code_400(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'BAD REQUESTS'}), '400 : BAD REQUESTS')

    def test_Error(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'BAD REQUESTS'})


if __name__ == '__main__':
    unittest.main()