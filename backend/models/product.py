from app import db, ma
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    # category is now a foreign key, but we keep the string for backward compatibility or display if needed, 
    # or we can remove it. Let's keep it simple and just add category_id and make category string optional/computed.
    # For this phase, I'll replace the string column with a relationship.
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref='products')
    
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'category': self.category.name if self.category else "Uncategorized",
            'category_id': self.category_id,
            'price': self.price,
            'stock': self.stock,
            'status': self.get_status(),
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def get_status(self):
        if self.stock == 0:
            return 'Out of Stock'
        elif self.stock <= self.low_stock_threshold:
            return 'Low Stock'
        else:
            return 'In Stock'

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
