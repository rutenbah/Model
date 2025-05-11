from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.cart import cart_bp
from app.models import Product, CartItem
from app import db

@cart_bp.route('/')
@login_required
def index():
    """Отображение корзины пользователя"""
    cart_items = current_user.cart_items.all()
    total = sum(item.subtotal for item in cart_items)
    return render_template('cart/index.html', cart_items=cart_items, total=total)

@cart_bp.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    """Добавление товара в корзину"""
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product_id:
        flash('Товар не выбран', 'danger')
        return redirect(url_for('catalog.index'))
    
    product = Product.query.get_or_404(product_id)
    
    # Проверяем, есть ли товар в корзине
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        # Обновляем количество, если товар уже в корзине
        cart_item.quantity += quantity
    else:
        # Создаем новый элемент корзины
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Товар добавлен в корзину', 'success')
    
    # Используем Accept заголовок для проверки AJAX-запроса
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'status': 'success', 'message': 'Товар добавлен в корзину'})
    
    return redirect(url_for('cart.index'))

@cart_bp.route('/update', methods=['POST'])
@login_required
def update_cart():
    """Обновление количества товара в корзине"""
    cart_item_id = request.form.get('cart_item_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not cart_item_id:
        flash('Элемент корзины не выбран', 'danger')
        return redirect(url_for('cart.index'))
    
    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=current_user.id).first_or_404()
    
    if quantity <= 0:
        # Удаляем элемент, если количество <= 0
        db.session.delete(cart_item)
        flash('Товар удален из корзины', 'info')
    else:
        # Обновляем количество
        cart_item.quantity = quantity
        flash('Корзина обновлена', 'success')
    
    db.session.commit()
    
    # Используем Accept заголовок для проверки AJAX-запроса
    if request.headers.get('Accept') == 'application/json':
        cart_items = current_user.cart_items.all()
        total = sum(item.subtotal for item in cart_items)
        return jsonify({
            'status': 'success', 
            'subtotal': cart_item.subtotal if quantity > 0 else 0,
            'total': total
        })
    
    return redirect(url_for('cart.index'))

@cart_bp.route('/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    """Удаление товара из корзины"""
    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    
    flash('Товар удален из корзины', 'info')
    
    # Используем Accept заголовок для проверки AJAX-запроса
    if request.headers.get('Accept') == 'application/json':
        cart_items = current_user.cart_items.all()
        total = sum(item.subtotal for item in cart_items)
        return jsonify({
            'status': 'success', 
            'total': total
        })
    
    return redirect(url_for('cart.index'))

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    """Очистка корзины"""
    current_user.cart_items.delete()
    db.session.commit()
    
    flash('Корзина очищена', 'info')
    
    # Используем Accept заголовок для проверки AJAX-запроса
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'status': 'success'})
    
    return redirect(url_for('cart.index')) 