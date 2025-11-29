from extensions import db, ma
from datetime import datetime
import pytz

# East Africa Time timezone
EAT = pytz.timezone('Africa/Nairobi')

def get_eat_now():
    """Get current time in East Africa Time"""
    return datetime.now(EAT)

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), default='cash')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=get_eat_now)
    
    # Relationships
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade="all, delete-orphan")
    user = db.relationship('User', backref='sales')

    def to_dict(self):
        # Handle both timezone-aware and naive datetimes
        created_at_str = None
        if self.created_at:
            if self.created_at.tzinfo is None:
                # Old data: naive datetime (assume UTC), convert to EAT
                created_at_eat = pytz.utc.localize(self.created_at).astimezone(EAT)
                created_at_str = created_at_eat.isoformat()
            else:
                # New data: already timezone-aware
                created_at_str = self.created_at.isoformat()
        
        return {
            'id': self.id,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else "Unknown",
            'items_count': len(self.items),
            'created_at': created_at_str,
            'items': [item.to_dict() for item in self.items]
        }

class SaleItem(db.Model):
    __tablename__ = 'sale_items'

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_sale = db.Column(db.Float, nullable=False)
    
    # Relationship
    product = db.relationship('Product')

    def to_dict(self):
        product_dict = None
        if self.product:
            product_dict = {
                'id': self.product.id,
                'name': self.product.name,
                'category': {
                    'id': self.product.category.id,
                    'name': self.product.category.name
                } if self.product.category else None
            }
        
        return {
            'id': self.id,
            'product_name': self.product.name if self.product else "Unknown Product",
            'product': product_dict,
            'quantity': self.quantity,
            'price_at_sale': self.price_at_sale,
            'subtotal': self.quantity * self.price_at_sale
        }

class SaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sale
        load_instance = True

sale_schema = SaleSchema()
sales_schema = SaleSchema(many=True)
