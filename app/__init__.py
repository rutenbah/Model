# Пустой файл для инициализации пакета
# Все необходимое определено в app.py в корне проекта 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///food_delivery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Настройка авторизации
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Импорт моделей для Alembic
from app.models.user import User
from app.models.product import Product, Category
from app.models.cart import CartItem
from app.models.order import Order, OrderItem, OrderStatus, OrderStatusChange, PaymentMethod, DeliveryMethod 