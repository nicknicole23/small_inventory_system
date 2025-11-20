from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, validate, validates, ValidationError


class User(db.Model):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # User Credentials
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Personal Information
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    
    # Role and Status
    role = db.Column(
        db.String(20),
        nullable=False,
        default='staff',
        index=True
    )  # Options: 'admin', 'manager', 'staff'
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships (to be added when other models are created)
    # products = db.relationship('Product', backref='creator', lazy='dynamic')
    # transactions = db.relationship('Transaction', backref='performer', lazy='dynamic')
    
    def set_password(self, password):
        """
        Hash and set the user's password.
        
        Args:
            password (str): Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify the user's password.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email=True):
        """
        Convert user object to dictionary.
        
        Args:
            include_email (bool): Whether to include email in response
            
        Returns:
            dict: User data dictionary
        """
        data = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_email:
            data['email'] = self.email
            
        return data
    
    def get_full_name(self):
        """Return user's full name or username if name not set."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.username
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == 'admin'
    
    def is_manager(self):
        """Check if user has manager role."""
        return self.role == 'manager'
    
    def __repr__(self):
        """String representation of User."""
        return f'<User {self.username} ({self.role})>'


# Marshmallow Schemas for Serialization/Validation

class UserSchema(Schema):
    """Schema for user serialization."""
    
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    first_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(validate=validate.Length(max=50))
    role = fields.Str(validate=validate.OneOf(['admin', 'manager', 'staff']))
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        """Schema metadata."""
        ordered = True


class UserRegistrationSchema(Schema):
    """Schema for user registration validation."""
    
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        error_messages={'required': 'Username is required.'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required.'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={
            'required': 'Password is required.',
            'invalid': 'Password must be at least 6 characters long.'
        }
    )
    first_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(validate=validate.Length(max=50))
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'staff']),
        missing='staff'  # Default value
    )
    
    @validates('password')
    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
        
        # Optional: Add more password strength requirements
        # if not any(char.isdigit() for char in value):
        #     raise ValidationError('Password must contain at least one digit.')
        # if not any(char.isupper() for char in value):
        #     raise ValidationError('Password must contain at least one uppercase letter.')


class UserLoginSchema(Schema):
    """Schema for user login validation."""
    
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required.'}
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'Password is required.'}
    )


class UserUpdateSchema(Schema):
    """Schema for user update validation."""
    
    username = fields.Str(validate=validate.Length(min=3, max=80))
    email = fields.Email()
    first_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(validate=validate.Length(max=50))
    role = fields.Str(validate=validate.OneOf(['admin', 'manager', 'staff']))
    is_active = fields.Bool()
    password = fields.Str(validate=validate.Length(min=6))


# Schema instances for use in routes
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_update_schema = UserUpdateSchema()
