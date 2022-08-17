import logging
import proj_log.configs.server_conf_log as log_config

LOGGER = logging.getLogger(log_config.__name__)


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            LOGGER.critical(
                f'Попытка запуска сервера с указанием неподходящего порта '
                f'{value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
