from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.category import Category, category_schema, categories_schema
from sqlalchemy.exc import IntegrityError

category_bp = Blueprint('categories', __name__)

@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200

@category_bp.route('/', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    
    try:
        new_category = Category(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify(new_category.to_dict()), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Category already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@category_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    try:
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        
        db.session.commit()
        return jsonify(category.to_dict()), 200
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Category name already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Check if category has products
    if category.products:
        return jsonify({'error': 'Cannot delete category with associated products'}), 400
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
