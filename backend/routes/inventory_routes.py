from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.product import Product, product_schema, products_schema
from sqlalchemy.exc import IntegrityError

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    # Use to_dict to include the computed status
    return jsonify([p.to_dict() for p in products]), 200

@inventory_bp.route('/', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    
    try:
        # Handle category_id if provided, or look up category by name if string provided (optional)
        category_id = data.get('category_id')
        
        new_product = Product(
            name=data['name'],
            sku=data['sku'],
            category_id=category_id,
            price=float(data['price']),
            stock=int(data['stock']),
            description=data.get('description', '')
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify(new_product.to_dict()), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'SKU already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    try:
        product.name = data.get('name', product.name)
        product.sku = data.get('sku', product.sku)
        if 'category_id' in data:
            product.category_id = data['category_id']
            
        if 'price' in data:
            product.price = float(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])
        product.description = data.get('description', product.description)
        
        db.session.commit()
        return jsonify(product.to_dict()), 200
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'SKU already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    from models.sale import Sale, SaleItem
    from datetime import datetime, timedelta
    
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock <= Product.low_stock_threshold).count()
    out_of_stock = Product.query.filter(Product.stock == 0).count()
    
    # Calculate real sales statistics
    now = datetime.utcnow()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    
    # Current month sales
    current_month_sales = Sale.query.filter(Sale.created_at >= current_month_start).all()
    current_revenue = sum(float(sale.total_amount) for sale in current_month_sales)
    
    # Calculate units sold (sum of all sale item quantities)
    current_units = db.session.query(db.func.sum(SaleItem.quantity)).join(Sale).filter(
        Sale.created_at >= current_month_start
    ).scalar() or 0
    
    # Previous month sales
    prev_month_sales = Sale.query.filter(
        Sale.created_at >= last_month_start,
        Sale.created_at < current_month_start
    ).all()
    prev_revenue = sum(float(sale.total_amount) for sale in prev_month_sales)
    
    prev_units = db.session.query(db.func.sum(SaleItem.quantity)).join(Sale).filter(
        Sale.created_at >= last_month_start,
        Sale.created_at < current_month_start
    ).scalar() or 0
    
    # Calculate trends
    revenue_trend = 0
    if prev_revenue > 0:
        revenue_trend = ((current_revenue - prev_revenue) / prev_revenue) * 100
    elif current_revenue > 0:
        revenue_trend = 100
        
    units_trend = 0
    if prev_units > 0:
        units_trend = ((current_units - prev_units) / prev_units) * 100
    elif current_units > 0:
        units_trend = 100
    
    return jsonify({
        'total_products': total_products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'active_products': total_products - out_of_stock,
        'total_revenue': current_revenue,
        'revenue_trend': revenue_trend,
        'units_sold': int(current_units),
        'units_trend': units_trend
    }), 200
