from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.sale import Sale, SaleItem, sale_schema, sales_schema
from models.product import Product
from models.user import User
from datetime import datetime

sale_bp = Blueprint('sales', __name__)

@sale_bp.route('/', methods=['GET'])
@jwt_required()
def get_sales():
    sales = Sale.query.order_by(Sale.created_at.desc()).all()
    return jsonify([s.to_dict() for s in sales]), 200

@sale_bp.route('/', methods=['POST'])
@jwt_required()
def create_sale():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data.get('items'):
        return jsonify({'error': 'No items in sale'}), 400
        
    try:
        # Calculate total amount and verify stock first
        total_amount = 0
        sale_items_data = []
        
        for item in data['items']:
            product_id = item['product_id']
            quantity = item['quantity']
            
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': f'Product {product_id} not found'}), 404
                
            if product.stock < quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}. Available: {product.stock}'}), 400
                
            item_total = product.price * quantity
            total_amount += item_total
            
            sale_items_data.append({
                'product': product,
                'quantity': quantity,
                'price_at_sale': product.price
            })

        # Create Sale
        new_sale = Sale(
            user_id=current_user_id,
            total_amount=total_amount,
            payment_method=data.get('payment_method', 'cash')
        )
        db.session.add(new_sale)
        db.session.flush() # Get ID for new_sale

        # Create Sale Items and Update Stock
        for item_data in sale_items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Create SaleItem
            sale_item = SaleItem(
                sale_id=new_sale.id,
                product_id=product.id,
                quantity=quantity,
                price_at_sale=item_data['price_at_sale']
            )
            db.session.add(sale_item)
            
            # Update Stock
            product.stock -= quantity
            
        db.session.commit()
        return jsonify(new_sale.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sale_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_sale(id):
    sale = Sale.query.get_or_404(id)
    return jsonify(sale.to_dict()), 200

@sale_bp.route('/generate-sample-data', methods=['POST'])
@jwt_required()
def generate_sample_data():
    """Generate sample sales data for testing/demo purposes"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Check if sales already exist
        existing_sales = Sale.query.count()
        if existing_sales > 0:
            return jsonify({'message': 'Sales data already exists', 'count': existing_sales}), 200
        
        # Get all products
        products = Product.query.all()
        if not products:
            return jsonify({'error': 'No products available. Please add products first.'}), 400
        
        import random
        from datetime import timedelta
        
        sales_created = 0
        today = datetime.utcnow()
        
        # Generate 15 sample sales over the past 30 days
        for i in range(15):
            # Random date in the past 30 days
            days_ago = random.randint(0, 30)
            sale_date = today - timedelta(days=days_ago)
            
            # Select 1-4 random products for this sale
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, min(num_items, len(products)))
            
            total_amount = 0
            sale_items_data = []
            
            for product in selected_products:
                # Skip if product has no stock
                if product.stock <= 0:
                    continue
                    
                # Random quantity (1-3 items)
                quantity = random.randint(1, min(3, product.stock))
                item_total = float(product.price) * quantity
                total_amount += item_total
                
                sale_items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price_at_sale': float(product.price)
                })
            
            # Only create sale if we have items
            if not sale_items_data:
                continue
                
            # Create Sale
            payment_methods = ['cash', 'card', 'mobile']
            new_sale = Sale(
                user_id=current_user_id,
                total_amount=total_amount,
                payment_method=random.choice(payment_methods),
                created_at=sale_date
            )
            db.session.add(new_sale)
            db.session.flush()
            
            # Create Sale Items and Update Stock
            for item_data in sale_items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                
                sale_item = SaleItem(
                    sale_id=new_sale.id,
                    product_id=product.id,
                    quantity=quantity,
                    price_at_sale=item_data['price_at_sale']
                )
                db.session.add(sale_item)
                
                # Update Stock
                product.stock -= quantity
            
            sales_created += 1
        
        db.session.commit()
        return jsonify({
            'message': 'Sample sales data generated successfully',
            'sales_created': sales_created
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
