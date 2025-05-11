from app import app, db
from flask import redirect, url_for

# Регистрация модулей (Blueprint)
from app.catalog import catalog_bp
from app.cart import cart_bp
from app.order import order_bp
from app.auth import auth_bp

app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return redirect(url_for('catalog.index'))

if __name__ == '__main__':
    app.run(debug=True) 