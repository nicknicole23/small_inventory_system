import os
from flask import Flask
from flask_migrate import Migrate
from config import config
from extensions import db, jwt, ma, cors

# Initialize migrate separately
migrate = Migrate()


def create_app(config_name=None):
    """
    Application factory pattern for Flask app creation.
    
    Args:
        config_name (str): Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    # Enable CORS for frontend communication
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Import models to ensure they are registered with SQLAlchemy
    from models.user import User
    from models.category import Category
    from models.product import Product
    from models.sale import Sale, SaleItem

    # Register blueprints (routes)
    from routes.auth_routes import auth_bp
    from routes.inventory_routes import inventory_bp
    from routes.category_routes import category_bp
    from routes.sale_routes import sale_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(sale_bp, url_prefix='/api/sales')
    
    # JWT error handlers
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token', 'message': str(error)}, 422
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {'error': 'Missing authorization header', 'message': str(error)}, 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return {'error': 'Token has expired', 'message': 'Please log in again'}, 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_data):
        return {'error': 'Token has been revoked', 'message': 'Please log in again'}, 401
    
    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'Server is running'}, 200
    
    # Root route
    @app.route('/')
    def index():
        return {
            'message': 'Small Shop Inventory System API',
            'version': '1.0.0',
            'environment': config_name
        }, 200
    
    return app


# Create app instance for development server
if __name__ == '__main__':
    app = create_app('development')
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
