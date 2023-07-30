from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Import the API routes
from api import user, products, favorites

# , subscription, brand, store, kitchen, sales

# Register the API blueprints
app.register_blueprint(user.bp)
app.register_blueprint(products.bp)
app.register_blueprint(favorites.bp) 
# app.register_blueprint(subscription.bp)
# app.register_blueprint(brand.bp)
# app.register_blueprint(store.bp)
# app.register_blueprint(kitchen.bp)
# app.register_blueprint(sales.bp)

if __name__ == '__main__':
     app.run(port=6000, debug=True)

