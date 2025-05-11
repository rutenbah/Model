from app import app, db
from app.models import Category, Product
import random

def seed_data():
    # Очистка таблиц перед заполнением
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.commit()
    
    # Создание категорий
    categories = [
        Category(name='Овощи', description='Свежие овощи'),
        Category(name='Фрукты', description='Свежие фрукты и ягоды'),
        Category(name='Молочные продукты', description='Молоко, творог, сыры и другие молочные продукты'),
        Category(name='Мясо', description='Свежее мясо и птица'),
        Category(name='Хлеб', description='Хлебобулочные изделия'),
        Category(name='Напитки', description='Соки, воды, газированные напитки')
    ]
    
    db.session.add_all(categories)
    db.session.commit()
    
    # Продукты - овощи
    vegetables = [
        Product(
            name='Помидоры', 
            description='Спелые помидоры, выращенные в экологически чистом регионе.', 
            price=150.0, 
            stock=100, 
            rating=4.7, 
            manufacturer='ФермерПрод', 
            category_id=categories[0].id,
            image_path='/static/img/tomato.svg'
        ),
        Product(
            name='Огурцы', 
            description='Свежие огурцы, хрустящие и ароматные.', 
            price=120.0, 
            stock=150, 
            rating=4.5, 
            manufacturer='ФермерПрод', 
            category_id=categories[0].id,
            image_path='/static/img/vegetables.svg'
        ),
        Product(
            name='Картофель', 
            description='Отборный картофель для приготовления любимых блюд.', 
            price=60.0, 
            stock=200, 
            rating=4.8, 
            manufacturer='Овощторг', 
            category_id=categories[0].id,
            image_path='/static/img/vegetables.svg'
        ),
        Product(
            name='Морковь', 
            description='Сладкая морковь, богатая витаминами.', 
            price=80.0, 
            stock=120, 
            rating=4.6, 
            manufacturer='Овощторг', 
            category_id=categories[0].id,
            image_path='/static/img/vegetables.svg'
        )
    ]
    
    # Продукты - фрукты
    fruits = [
        Product(
            name='Яблоки', 
            description='Сочные яблоки сорта Голден.', 
            price=160.0, 
            stock=80, 
            rating=4.5, 
            manufacturer='ФруктыМир', 
            category_id=categories[1].id,
            image_path='/static/img/apple.svg'
        ),
        Product(
            name='Бананы', 
            description='Спелые и сладкие бананы.', 
            price=120.0, 
            stock=100, 
            rating=4.3, 
            manufacturer='ТропикИмпорт', 
            category_id=categories[1].id,
            image_path='/static/img/fruits.svg'
        ),
        Product(
            name='Апельсины', 
            description='Сочные и ароматные апельсины из Испании.', 
            price=180.0, 
            stock=70, 
            rating=4.7, 
            manufacturer='ТропикИмпорт', 
            category_id=categories[1].id,
            image_path='/static/img/fruits.svg'
        )
    ]
    
    # Продукты - молочные продукты
    dairy = [
        Product(
            name='Молоко', 
            description='Свежее пастеризованное молоко 3.2% жирности.', 
            price=90.0, 
            stock=150, 
            rating=4.8, 
            manufacturer='МолокоФерма', 
            category_id=categories[2].id,
            image_path='/static/img/milk.svg'
        ),
        Product(
            name='Творог', 
            description='Нежный творог 9% жирности.', 
            price=130.0, 
            stock=80, 
            rating=4.6, 
            manufacturer='МолокоФерма', 
            category_id=categories[2].id,
            image_path='/static/img/dairy.svg'
        ),
        Product(
            name='Сыр Российский', 
            description='Классический твердый сыр Российский, 45% жирности.', 
            price=400.0, 
            stock=50, 
            rating=4.7, 
            manufacturer='СырМастер', 
            category_id=categories[2].id,
            image_path='/static/img/dairy.svg'
        )
    ]
    
    # Продукты - мясо
    meat = [
        Product(
            name='Куриное филе', 
            description='Охлажденное куриное филе высшего сорта.', 
            price=320.0, 
            stock=70, 
            rating=4.9, 
            manufacturer='ПтицаФерма', 
            category_id=categories[3].id,
            image_path='/static/img/meat.svg'
        ),
        Product(
            name='Говядина', 
            description='Мраморная говядина для стейков и других блюд.', 
            price=650.0, 
            stock=40, 
            rating=4.8, 
            manufacturer='МясоПром', 
            category_id=categories[3].id,
            image_path='/static/img/meat.svg'
        ),
        Product(
            name='Свинина', 
            description='Свежая свинина, мякоть без кости.', 
            price=480.0, 
            stock=60, 
            rating=4.6, 
            manufacturer='МясоПром', 
            category_id=categories[3].id,
            image_path='/static/img/meat.svg'
        )
    ]
    
    # Продукты - хлеб
    bread = [
        Product(
            name='Хлеб белый', 
            description='Свежий белый хлеб из муки высшего сорта.', 
            price=45.0, 
            stock=100, 
            rating=4.5, 
            manufacturer='ХлебЗавод', 
            category_id=categories[4].id,
            image_path='/static/img/bread.svg'
        ),
        Product(
            name='Батон нарезной', 
            description='Классический нарезной батон.', 
            price=50.0, 
            stock=80, 
            rating=4.4, 
            manufacturer='ХлебЗавод', 
            category_id=categories[4].id,
            image_path='/static/img/bread.svg'
        ),
        Product(
            name='Хлеб ржаной', 
            description='Традиционный ржаной хлеб.', 
            price=55.0, 
            stock=70, 
            rating=4.7, 
            manufacturer='ХлебДом', 
            category_id=categories[4].id,
            image_path='/static/img/bread.svg'
        )
    ]
    
    # Продукты - напитки
    drinks = [
        Product(
            name='Сок апельсиновый', 
            description='Натуральный сок из свежих апельсинов, без добавления сахара.', 
            price=140.0, 
            stock=90, 
            rating=4.6, 
            manufacturer='СокДар', 
            category_id=categories[5].id,
            image_path='/static/img/drinks.svg'
        ),
        Product(
            name='Минеральная вода', 
            description='Природная минеральная вода, газированная.', 
            price=70.0, 
            stock=120, 
            rating=4.5, 
            manufacturer='АкваМир', 
            category_id=categories[5].id,
            image_path='/static/img/drinks.svg'
        ),
        Product(
            name='Лимонад', 
            description='Освежающий газированный напиток с натуральными ингредиентами.', 
            price=95.0, 
            stock=80, 
            rating=4.3, 
            manufacturer='НапиткиПлюс', 
            category_id=categories[5].id,
            image_path='/static/img/drinks.svg'
        )
    ]
    
    # Добавление всех продуктов в базу данных
    all_products = vegetables + fruits + dairy + meat + bread + drinks
    db.session.add_all(all_products)
    db.session.commit()
    
    print('База данных успешно заполнена тестовыми данными!')

if __name__ == '__main__':
    with app.app_context():
        seed_data() 