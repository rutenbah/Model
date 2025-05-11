from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.order import order_bp
from app.models import Product, CartItem, Order, OrderItem, OrderStatus, OrderStatusChange, PaymentMethod, DeliveryMethod
from app import db
from datetime import datetime

@order_bp.route('/checkout')
@login_required
def checkout():
    """Страница оформления заказа"""
    cart_items = current_user.cart_items.all()
    
    if not cart_items:
        flash('Корзина пуста. Добавьте товары для оформления заказа.', 'warning')
        return redirect(url_for('catalog.index'))
    
    total = sum(item.subtotal for item in cart_items)
    
    return render_template(
        'order/checkout.html',
        cart_items=cart_items,
        total=total,
        payment_methods=PaymentMethod,
        delivery_methods=DeliveryMethod
    )

@order_bp.route('/create', methods=['POST'])
@login_required
def create_order():
    """Создание заказа"""
    # Получение данных из формы
    delivery_address = request.form.get('delivery_address')
    payment_method = request.form.get('payment_method')
    delivery_method = request.form.get('delivery_method')
    
    # Проверка наличия необходимых данных
    if not delivery_address or not payment_method or not delivery_method:
        flash('Пожалуйста, заполните все обязательные поля', 'danger')
        return redirect(url_for('order.checkout'))
    
    # Получение товаров из корзины
    cart_items = current_user.cart_items.all()
    
    if not cart_items:
        flash('Корзина пуста. Добавьте товары для оформления заказа.', 'warning')
        return redirect(url_for('catalog.index'))
    
    # Расчет общей стоимости
    total_amount = sum(item.subtotal for item in cart_items)
    
    # Создание заказа
    order = Order(
        user_id=current_user.id,
        status=OrderStatus.CREATED,
        total_amount=total_amount,
        delivery_address=delivery_address,
        payment_method=PaymentMethod[payment_method],
        delivery_method=DeliveryMethod[delivery_method]
    )
    
    # Добавление элементов заказа
    for cart_item in cart_items:
        order_item = OrderItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        order.items.append(order_item)
    
    # Добавление записи о смене статуса
    status_change = OrderStatusChange(
        new_status=OrderStatus.CREATED
    )
    order.status_changes.append(status_change)
    
    # Сохранение заказа и очистка корзины
    db.session.add(order)
    current_user.cart_items.delete()
    db.session.commit()
    
    flash('Заказ успешно оформлен!', 'success')
    return redirect(url_for('order.order_detail', order_id=order.id))

@order_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    """Детальная информация о заказе"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order/detail.html', order=order)

@order_bp.route('/list')
@login_required
def order_list():
    """Список заказов пользователя"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    orders = Order.query.filter_by(user_id=current_user.id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return render_template('order/list.html', orders=orders)

@order_bp.route('/track/<int:order_id>')
@login_required
def track_order(order_id):
    """Отслеживание статуса заказа"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    status_changes = order.status_changes
    
    return render_template('order/track.html', order=order, status_changes=status_changes)

@order_bp.route('/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Отмена заказа"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    # Проверка, можно ли отменить заказ
    if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
        flash('Невозможно отменить заказ в текущем статусе', 'danger')
        return redirect(url_for('order.order_detail', order_id=order.id))
    
    # Изменение статуса заказа
    old_status = order.status
    order.status = OrderStatus.CANCELLED
    
    # Добавление записи о смене статуса
    status_change = OrderStatusChange(
        order_id=order.id,
        old_status=old_status,
        new_status=OrderStatus.CANCELLED
    )
    
    db.session.add(status_change)
    db.session.commit()
    
    flash('Заказ отменен', 'info')
    return redirect(url_for('order.order_detail', order_id=order.id)) 