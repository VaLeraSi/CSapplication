"""Config server logging"""

import sys
import logging.handlers

from pathlib import Path

from common.variables import LOGGING_LEVEL

# Получаем имя директории на 2 уровня выше и добавляем к пути директорию для логов
LOG_DIR = Path(__file__).resolve().parent.parent / 'logs'
# Подготовка имени файла для логирования
LOG_FILE_NAME = 'server.log'

# если директории нет создаём её
if not LOG_DIR.exists():
    LOG_DIR.mkdir()

# создаём формировщик логов (formatter):
SERVER_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
PATH = LOG_DIR / LOG_FILE_NAME

# создаём потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
