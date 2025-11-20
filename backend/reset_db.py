from app import create_app, db
from models.user import User
from models.category import Category
from models.product import Product
from models.sale import Sale, SaleItem

app = create_app('development')

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating all tables...")
    db.create_all()
    
    print("Seeding initial data...")
    
    # Create default categories
    categories = [
        Category(name='Electronics', description='Gadgets and devices'),
        Category(name='Clothing', description='Apparel and fashion'),
        Category(name='Groceries', description='Daily essentials'),
        Category(name='Other', description='Miscellaneous items')
    ]
    
    for cat in categories:
        db.session.add(cat)
        
    db.session.commit()
    print("Database reset and seeded successfully!")
