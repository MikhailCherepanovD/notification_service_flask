from dotenv import load_dotenv
from app.log.logging_config import setup_logging
from app import app

load_dotenv()  # Загружает переменные окружения из файла .env

if __name__ == '__main__':
    setup_logging()
    app.run(host="0.0.0.0", port=8082)