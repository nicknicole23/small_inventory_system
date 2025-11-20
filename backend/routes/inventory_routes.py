from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
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
        new_product = Product(
            name=data['name'],
            sku=data['sku'],
            category=data['category'],
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
        product.category = data.get('category', product.category)
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
