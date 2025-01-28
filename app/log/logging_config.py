import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app/log/app.log',  # Запись в файл
        filemode='w'  # Режим добавления a / режим перезаписи w
    )

    # Создаем фильтр для исключения запросов к статическим файлам
    class StaticFilesFilter(logging.Filter):
        def filter(self, record):
            return '/static/' not in record.getMessage()

    # Настройка логгера Werkzeug
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)  # Уровень логирования
    werkzeug_logger.addFilter(StaticFilesFilter())  # Применение фильтра