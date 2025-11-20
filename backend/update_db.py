from app import create_app, db
from models.product import Product

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully!")
