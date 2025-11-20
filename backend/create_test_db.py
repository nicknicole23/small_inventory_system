#!/usr/bin/env python3
"""
Create test database with sample data
"""
from app import create_app, db
from models.user import User
from models.category import Category
from models.product import Product
from werkzeug.security import generate_password_hash

def create_test_db():
    app = create_app('development')

    with app.app_context():
        # Drop and recreate all tables
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        # Create test user
        print("Creating test user...")
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123'),
            first_name='Test',
            last_name='User',
            role='admin',
            is_active=True
        )
        db.session.add(test_user)
        
        # Create categories
        print("Creating categories...")
        categories = [
            Category(name='Electronics', description='Electronic devices and accessories'),
            Category(name='Clothing', description='Apparel and fashion items'),
            Category(name='Groceries', description='Food and daily essentials'),
            Category(name='Books', description='Books and educational materials'),
            Category(name='Toys', description='Toys and games'),
        ]
        for cat in categories:
            db.session.add(cat)
        
        db.session.commit()
        
        # Create test products
        print("Creating test products...")
        products = [
            Product(name='Laptop', sku='LAP001', category_id=1, price=999.99, stock=15, low_stock_threshold=5, description='High-performance laptop'),
            Product(name='Smartphone', sku='PHN001', category_id=1, price=699.99, stock=25, low_stock_threshold=10, description='Latest smartphone model'),
            Product(name='Headphones', sku='AUD001', category_id=1, price=149.99, stock=50, low_stock_threshold=15, description='Wireless headphones'),
            Product(name='T-Shirt', sku='CLO001', category_id=2, price=19.99, stock=100, low_stock_threshold=20, description='Cotton t-shirt'),
            Product(name='Jeans', sku='CLO002', category_id=2, price=49.99, stock=75, low_stock_threshold=15, description='Denim jeans'),
            Product(name='Rice 5kg', sku='GRO001', category_id=3, price=12.99, stock=200, low_stock_threshold=50, description='Premium quality rice'),
            Product(name='Cooking Oil 2L', sku='GRO002', category_id=3, price=8.99, stock=150, low_stock_threshold=30, description='Vegetable cooking oil'),
            Product(name='Python Book', sku='BOK001', category_id=4, price=39.99, stock=30, low_stock_threshold=10, description='Learn Python programming'),
            Product(name='Action Figure', sku='TOY001', category_id=5, price=24.99, stock=60, low_stock_threshold=15, description='Superhero action figure'),
            Product(name='Board Game', sku='TOY002', category_id=5, price=34.99, stock=40, low_stock_threshold=10, description='Family board game'),
        ]
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ Test database created successfully!")
        print("="*50)
        print("\nTest User Credentials:")
        print("  Email: test@example.com")
        print("  Password: password123")
        print("\nDatabase Summary:")
        print(f"  - Categories: {len(categories)}")
        print(f"  - Products: {len(products)}")
        print(f"  - Users: 1")
        print("\nDatabase location: backend/instance/inventory.db")
        print("="*50)

if __name__ == '__main__':
    create_test_db()
