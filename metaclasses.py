import dis

# Метакласс для проверки соответствия сервера:
from pprint import pprint


class ClientVerifier(type):
    def __init__(cls, classname, classparent, classdict):
        methods = []

        for func in classdict:
            try:
                ret = dis.get_instructions(classdict[func])
                # Если не функция то ловим исключение
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)

        print(20 * '-', 'methods', 20 * '-')
        pprint(methods)
        for command in ('accept', 'listen'):
            if command in methods:
                raise TypeError('Запрещеночка. Используется недопустимый метод.')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(classname, classparent, classdict)


class ServerVarifier(type):
    def __init__(cls, classname, classparent, classdict):
        # Список методов, которые используются в функциях класса:
        methods = []
        # Обычно методы, обёрнутые декораторами попадают
        methods_2 = []
        # Атрибуты, используемые в функциях классов
        attrs = []
        # перебираем ключи
        for func in classdict:
            try:
                # Возвращает итератор по инструкциям в предоставленной функции
                # , методе, строке исходного кода или объекте кода.
                ret = dis.get_instructions(classdict[func])
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы и атрибуты.
                for i in ret:
                    print(i)
                    # i - Instruction(opname='LOAD_GLOBAL', opcode=116, arg=9, argval='send_message',
                    # argrepr='send_message', offset=308, starts_line=201, is_jump_target=False)
                    # opname - имя для операции
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            # заполняем список методами, использующимися в функциях класса
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_2:
                            # заполняем список атрибутами, использующимися в функциях класса
                            methods_2.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            # заполняем список атрибутами, использующимися в функциях класса
                            attrs.append(i.argval)
        print(20*'-', 'methods', 20*'-')
        pprint(methods)
        print(20*'-', 'methods_2', 20*'-')
        pprint(methods_2)
        print(20*'-', 'attrs', 20*'-')
        pprint(attrs)
        print(50*'-')
        # Если обнаружено использование недопустимого метода connect, вызываем исключение:
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        # Если сокет не инициализировался константами SOCK_STREAM(TCP) AF_INET(IPv4), тоже исключение.
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        # Обязательно вызываем конструктор предка:
        super().__init__(classname, classparent, classdict)