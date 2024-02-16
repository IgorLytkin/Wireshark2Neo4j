import logging
import sys

logger = logging.getLogger(__name__)
print(logger.handlers)
stderr_handler = logging.StreamHandler()
stdout_handler = logging.StreamHandler(sys.stdout)

# Определяем первый вид форматирования
format_1 = '#%(levelname)-8s [%(asctime)s] - %(filename)s:' \
           '%(lineno)d - %(name)s - %(message)s'
# Определяем второй вид форматирования
format_2 = '[{asctime}] #{levelname:8} {filename}:' \
           '{lineno} - {name} - {message}'

# Инициализируем первый форматтер
formatter_1 = logging.Formatter(fmt=format_1)
# Инициализируем второй форматтер
formatter_2 = logging.Formatter(
    fmt=format_2,
    style='{'
)

# Создаем логгер
logger = logging.getLogger(__name__)

# Инициализируем хэндлер, который будет перенаправлять логи в stderr
stderr_handler = logging.StreamHandler()
# Инициализируем хэндлер, который будет перенаправлять логи в stdout
stdout_handler = logging.StreamHandler(sys.stdout)

# Устанавливаем форматтеры для хэндлеров
stderr_handler.setFormatter(formatter_1)
stdout_handler.setFormatter(formatter_2)

# Добавляем хэндлеры логгеру
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)

# Создаем лог
logger.warning('Это лог с предупреждением!')

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logs.log')
logger.addHandler(file_handler)
print(logger.handlers)
logger.warning('Это лог с предупреждением!')

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)
print(logger.handlers)
logger.warning('Это лог с предупреждением!')

logging.debug('Это лог уровня DEBUG')
logging.info('Это лог уровня INFO')
logging.warning('Это лог уровня WARNING')
logging.error('Это лог уровня ERROR')
logging.critical('Это лог уровня CRITICAL')

print(logging.DEBUG)
print(logging.INFO)
print(logging.WARNING)
print(logging.ERROR)
print(logging.CRITICAL)

logging.basicConfig(level=logging.DEBUG)

logging.debug('Это лог уровня DEBUG')
logging.info('Это лог уровня INFO')
logging.warning('Это лог уровня WARNING')
logging.error('Это лог уровня ERROR')
logging.critical('Это лог уровня CRITICAL')

logging.basicConfig(level=logging.CRITICAL)

logging.debug('Это лог уровня DEBUG')
logging.info('Это лог уровня INFO')
logging.warning('Это лог уровня WARNING')
logging.error('Это лог уровня ERROR')
logging.critical('Это лог уровня CRITICAL')

logger_1 = logging.getLogger('one.two')
print(logger_1.parent)
logger_2 = logging.getLogger('one.two.three')
print(logger_2.parent)

logger = logging.getLogger(__name__)
logger.warning('Предупреждение!')
logger.debug('Отладочная информация')

# format='[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s'
format='[{asctime}] #{levelname:8} {filename}:{lineno} - {name} - {message}'


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.debug('Лог уровня DEBUG')

logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)
logger = logging.getLogger(__name__)
logger.debug('Лог уровня DEBUG')

format_1 = '#%(levelname)-8s [%(asctime)s] - %(filename)s:' \
           '%(lineno)d - %(name)s - %(message)s'
format_2 = '[{asctime}] #{levelname:8} {filename}:' \
           '{lineno} - {name} - {message}'

formatter_1 = logging.Formatter(fmt=format_1)
formatter_2 = logging.Formatter(
    fmt=format_2,
    style='{'
)

# Определяем свой фильтр, наследуюясь от класса Filter библиотеки logging
class EvenLogFilter(logging.Filter):
    def filter(self, record):
        return not record.i % 2


# Инициализируем логгер
logger = logging.getLogger(__name__)

# Создаем хэндлер, который будет направлять логи в stderr
stderr_handler = logging.StreamHandler()

# Подключаем фильтр к хэндлеру
stderr_handler.addFilter(EvenLogFilter())

# Подключаем хэндлер к логгеру
logger.addHandler(stderr_handler)

for i in range(1, 5):
    logger.warning('Важно! Это лог с предупреждением! %d', i, extra={'i': i})


    # Определяем свой фильтр, наследуюясь от класса Filter библиотеки logging
class ErrorLogFilter(logging.Filter):
    # Переопределяем метод filter, который принимает `self` и `record`
    # Переменная рекорд будет ссылаться на объект класса LogRecord
    def filter(self, record):
        print(dir(record))
        return record.levelname == 'ERROR' and 'важно' in record.msg.lower()


# Инициализируем логгер
logger = logging.getLogger(__name__)

# Создаем хэндлер, который будет направлять логи в stderr
stderr_handler = logging.StreamHandler()

# Подключаем фильтр к хэндлеру
stderr_handler.addFilter(ErrorLogFilter())

# Подключаем хэндлер к логгеру
logger.addHandler(stderr_handler)

logger.warning('Важно! Это лог с предупреждением!')
logger.error('Важно! Это лог с ошибкой!')
logger.info('Важно! Это лог с уровня INFO!')
logger.error('Это лог с ошибкой!')
