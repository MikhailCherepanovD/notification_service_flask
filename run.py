from dotenv import load_dotenv
from app.log.logging_config import setup_logging
from app import app  # Здесь уже есть готовый Flask app
from flask_session import Session
import tempfile

# Для хранения сессий на сервере, а не в браузере
session_dir = tempfile.mkdtemp()
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = session_dir
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SECRET_KEY"] = "supersecretkey"
Session(app)

load_dotenv()  # Загружает переменные окружения из .env

if __name__ == "__main__":
    setup_logging()
    app.run(host="0.0.0.0", port=8082)
