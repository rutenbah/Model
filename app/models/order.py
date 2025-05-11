from datetime import datetime
from app import db
import enum

class OrderStatus(enum.Enum):
    CREATED = 'created'
    PROCESSING = 'processing'
    SHIPPING = 'shipping'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class PaymentMethod(enum.Enum):
    CREDIT_CARD = 'credit_card'
    CASH = 'cash'
    BANK_TRANSFER = 'bank_transfer'
    ONLINE_PAYMENT = 'online_payment'

class DeliveryMethod(enum.Enum):
    STANDARD = 'standard'
    EXPRESS = 'express'
    PICKUP = 'pickup'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.CREATED)
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(256))
    payment_method = db.Column(db.Enum(PaymentMethod))
    delivery_method = db.Column(db.Enum(DeliveryMethod))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с элементами заказа
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'
    
    @property
    def calculate_total(self):
        return sum(item.subtotal for item in self.items)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)  # Цена на момент заказа
    
    # Связь с товаром
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<OrderItem {self.product.name} ({self.quantity})>'
    
    @property
    def subtotal(self):
        return self.price * self.quantity

class OrderStatusChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    old_status = db.Column(db.Enum(OrderStatus), nullable=True)
    new_status = db.Column(db.Enum(OrderStatus), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с заказом
    order = db.relationship('Order', backref='status_changes') 