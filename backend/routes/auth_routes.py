from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON:
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "securepassword",
            "first_name": "John",
            "last_name": "Doe",
            "role": "staff"  // optional, defaults to "staff"
        }
    
    Returns:
        201: User created successfully
        400: Validation error or user already exists
        500: Server error
    """
    # Import inside function to avoid circular imports
    from extensions import db
    from models.user import User, user_registration_schema, user_schema
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate input data
        try:
            validated_data = user_registration_schema.load(data)
        except ValidationError as err:
            return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == validated_data['username']) |
            (User.email == validated_data['email'])
        ).first()
        
        if existing_user:
            if existing_user.username == validated_data['username']:
                return jsonify({'error': 'Username already exists'}), 400
            if existing_user.email == validated_data['email']:
                return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        new_user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            role=validated_data.get('role', 'staff')
        )
        
        # Hash and set password
        new_user.set_password(validated_data['password'])
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Return success response
        return jsonify({
            'message': 'User registered successfully',
            'user': user_schema.dump(new_user)
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error', 'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred during registration', 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT tokens.
    
    Expected JSON:
        {
            "email": "john@example.com",
            "password": "securepassword"
        }
    
    Returns:
        200: Login successful with access and refresh tokens
        400: Validation error
        401: Invalid credentials
        403: Account inactive
        500: Server error
    """
    # Import inside function to avoid circular imports
    from models.user import User, user_schema, user_login_schema
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate input data
        try:
            validated_data = user_login_schema.load(data)
        except ValidationError as err:
            return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
        
        # Find user by email
        user = User.query.filter_by(email=validated_data['email']).first()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not user.check_password(validated_data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if account is active
        if not user.is_active:
            return jsonify({'error': 'Account is inactive. Please contact administrator.'}), 403
        
        # Create JWT tokens
        # Include additional claims in the token
        additional_claims = {
            'role': user.role,
            'username': user.username
        }
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        
        # Return tokens and user info
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_schema.dump(user)
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during login', 'message': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Returns:
        200: New access token
        401: Invalid or expired refresh token
    """
    # Import inside function to avoid circular imports
    from models.user import User
    
    try:
        # Get current user identity from refresh token
        current_user_id = get_jwt_identity()
        
        # Get user from database to ensure they still exist and are active
        user = User.query.get(int(current_user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Create new access token
        additional_claims = {
            'role': user.role,
            'username': user.username
        }
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'An error occurred during token refresh', 'message': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (invalidate token).
    
    Note: JWT tokens are stateless. For production, implement token blacklist.
    This endpoint is here for client-side logout handling.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Logout successful
    """
    # In production, you would:
    # 1. Add token to blacklist/revoked tokens list
    # 2. Store in Redis or database
    # 3. Check blacklist on each protected request
    
    # For now, client should remove tokens from storage
    return jsonify({'message': 'Logout successful. Please remove tokens from client.'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user's information.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: User information
        401: Unauthorized
        404: User not found
    """
    # Import inside function to avoid circular imports
    from models.user import User, user_schema
    
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        
        # Get user from database
        user = User.query.get(int(current_user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 403
        
        return jsonify({
            'user': user_schema.dump(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    Change user password.
    
    Expected JSON:
        {
            "current_password": "oldpassword",
            "new_password": "newpassword"
        }
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Password changed successfully
        400: Validation error
        401: Invalid current password
    """
    try:
        # Get current user ID from JWT
        current_user_id = int(get_jwt_identity())
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': 'New password must be at least 6 characters long'}), 400
        
        # Import inside function to avoid circular imports
        from extensions import db
        from models.user import User
        
        # Get user from database
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Set new password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile information.
    
    Expected JSON:
        {
            "username": "new_username",
            "email": "new_email@example.com",
            "first_name": "FirstName",
            "last_name": "LastName"
        }
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Profile updated successfully
        400: Validation error or duplicate username/email
        404: User not found
    """
    try:
        # Get current user ID from JWT
        current_user_id = int(get_jwt_identity())
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Import inside function to avoid circular imports
        from extensions import db
        from models.user import User, user_schema
        
        # Get user from database
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if username is being changed and if it's already taken
        if 'username' in data and data['username'] != user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                return jsonify({'error': 'Username already exists'}), 400
            user.username = data['username']
        
        # Check if email is being changed and if it's already taken
        if 'email' in data and data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({'error': 'Email already exists'}), 400
            user.email = data['email']
        
        # Update other fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user_schema.dump(user)
        }), 200
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


# Error handlers for JWT
@auth_bp.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized access."""
    return jsonify({'error': 'Unauthorized access'}), 401


@auth_bp.errorhandler(403)
def forbidden(error):
    """Handle forbidden access."""
    return jsonify({'error': 'Access forbidden'}), 403
