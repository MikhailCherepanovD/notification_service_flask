from flask import Flask
from config import DevelopmentConfig

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на случайную строку
app.config.from_object(DevelopmentConfig)

from app import routes