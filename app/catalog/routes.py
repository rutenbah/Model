from flask import render_template, request, jsonify, redirect, url_for, flash
from app.catalog import catalog_bp
from app.models import Product, Category
from app import db
from sqlalchemy import or_

@catalog_bp.route('/')
def index():
    """Отображение всех товаров в каталоге"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    products = Product.query.paginate(page=page, per_page=per_page)
    categories = Category.query.all()
    return render_template('catalog/index.html', products=products, categories=categories)

@catalog_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Отображение детальной информации о товаре"""
    product = Product.query.get_or_404(product_id)
    return render_template('catalog/product_detail.html', product=product)

@catalog_bp.route('/category/<int:category_id>')
def category_products(category_id):
    """Отображение товаров по категории"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).paginate(page=page, per_page=per_page)
    categories = Category.query.all()
    return render_template('catalog/index.html', products=products, categories=categories, current_category=category)

@catalog_bp.route('/search')
def search():
    """Поиск товаров по различным критериям"""
    query = request.args.get('q', '')
    category_id = request.args.get('category', type=int)
    manufacturer = request.args.get('manufacturer')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    sort_by = request.args.get('sort_by', 'name')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    # Базовый запрос
    products_query = Product.query
    
    # Фильтрация по поисковому запросу
    if query:
        products_query = products_query.filter(
            or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            )
        )
    
    # Фильтрация по категории
    if category_id:
        products_query = products_query.filter_by(category_id=category_id)
    
    # Фильтрация по производителю
    if manufacturer:
        products_query = products_query.filter_by(manufacturer=manufacturer)
    
    # Фильтрация по цене
    if min_price is not None:
        products_query = products_query.filter(Product.price >= min_price)
    if max_price is not None:
        products_query = products_query.filter(Product.price <= max_price)
    
    # Фильтрация по рейтингу
    if min_rating is not None:
        products_query = products_query.filter(Product.rating >= min_rating)
    
    # Сортировка
    if sort_by == 'price_asc':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        products_query = products_query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        products_query = products_query.order_by(Product.rating.desc())
    else:  # По умолчанию сортировка по имени
        products_query = products_query.order_by(Product.name)
    
    # Пагинация
    products = products_query.paginate(page=page, per_page=per_page)
    categories = Category.query.all()
    manufacturers = db.session.query(Product.manufacturer).distinct().all()
    
    return render_template(
        'catalog/search.html', 
        products=products, 
        categories=categories, 
        manufacturers=manufacturers,
        query=query,
        category_id=category_id,
        manufacturer=manufacturer,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        sort_by=sort_by
    )

@catalog_bp.route('/api/products')
def api_products():
    """API для получения товаров в формате JSON"""
    products = [product.to_dict() for product in Product.query.all()]
    return jsonify(products) 