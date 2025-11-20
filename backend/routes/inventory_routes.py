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
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock <= Product.low_stock_threshold).count()
    out_of_stock = Product.query.filter(Product.stock == 0).count()
    
    # Calculate total inventory value as a proxy for "Revenue" for now, 
    # or just return mock data for sales since we don't have a Sales model yet.
    # Let's return real inventory stats and mock sales stats.
    
    return jsonify({
        'total_products': total_products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'active_products': total_products - out_of_stock
    }), 200
