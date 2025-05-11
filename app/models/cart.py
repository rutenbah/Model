from datetime import datetime
from app import db

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    product = db.relationship('Product')
    user = db.relationship('User', backref=db.backref('cart_items', lazy='dynamic'))
    
    def __repr__(self):
        return f'<CartItem {self.product.name} ({self.quantity})>'
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity 