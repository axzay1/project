from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Import the API routes
from api import user, products, favorites



# Register the API blueprints
app.register_blueprint(user.bp)
app.register_blueprint(products.bp)
app.register_blueprint(favorites.bp) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)

