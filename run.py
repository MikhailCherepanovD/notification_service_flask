from dotenv import load_dotenv
from app.log.logging_config import setup_logging
from app import app  # Здесь уже есть готовый Flask app
from flask_session import Session
import os
import tempfile


load_dotenv()  # Загружает переменные окружения из .env
# Для хранения сессий на сервере, а не в браузере
session_dir = tempfile.mkdtemp()
app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE")
app.config["SESSION_FILE_DIR"] = session_dir
app.config["SESSION_PERMANENT"] = os.getenv("SESSION_PERMANENT")
app.config["SESSION_USE_SIGNER"] = os.getenv("SESSION_USE_SIGNER")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
Session(app)



if __name__ == "__main__":
    setup_logging()
    app.run(host=os.getenv("THIS_HOST"), port=os.getenv("THIS_PORT"))
