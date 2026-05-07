#!/usr/bin/env python3
"""
Sample Backend API using Flask
A basic REST API for user management with CRUD operations

Author: Backend Team
Version: 1.0.0
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Configuration
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'
app.config['HOST'] = os.getenv('API_HOST', '0.0.0.0')
app.config['PORT'] = int(os.getenv('API_PORT', 5000))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory database (replace with actual database in production)
users_db = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'role': 'admin',
        'created_at': '2024-01-01T10:00:00Z'
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'role': 'user',
        'created_at': '2024-01-02T14:30:00Z'
    }
]

next_user_id = 3

# Utility functions
def get_current_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + 'Z'

def validate_user_data(data):
    """Validate user input data"""
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return False, f"Field '{field}' is required"
    
    if '@' not in data['email']:
        return False, "Invalid email format"
    
    return True, "Valid"

def find_user_by_id(user_id):
    """Find user by ID"""
    return next((user for user in users_db if user['id'] == user_id), None)

# API Routes

@app.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint"""
    return jsonify({
        'message': 'Welcome to Backend API!',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': get_current_timestamp(),
        'endpoints': {
            'health': '/health',
            'users': '/api/users',
            'docs': 'https://github.com/dhruv639508/backend'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': get_current_timestamp(),
        'uptime': 'running',
        'version': '1.0.0'
    }), 200

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users with optional filtering"""
    try:
        # Optional filtering by role
        role_filter = request.args.get('role')
        filtered_users = users_db
        
        if role_filter:
            filtered_users = [user for user in users_db if user['role'].lower() == role_filter.lower()]
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_users = filtered_users[start_idx:end_idx]
        
        return jsonify({
            'success': True,
            'data': paginated_users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(filtered_users),
                'pages': (len(filtered_users) + per_page - 1) // per_page
            },
            'timestamp': get_current_timestamp()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'timestamp': get_current_timestamp()
        }), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Get a specific user by ID"""
    try:
        user = find_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': f'User with ID {user_id} not found',
                'timestamp': get_current_timestamp()
            }), 404
        
        return jsonify({
            'success': True,
            'data': user,
            'timestamp': get_current_timestamp()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'timestamp': get_current_timestamp()
        }), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        global next_user_id
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided',
                'timestamp': get_current_timestamp()
            }), 400
        
        # Validate input
        is_valid, message = validate_user_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': message,
                'timestamp': get_current_timestamp()
            }), 400
        
        # Check for duplicate email
        existing_user = next((user for user in users_db if user['email'].lower() == data['email'].lower()), None)
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'User with this email already exists',
                'timestamp': get_current_timestamp()
            }), 409
        
        # Create new user
        new_user = {
            'id': next_user_id,
            'name': data['name'].strip(),
            'email': data['email'].strip().lower(),
            'role': data.get('role', 'user').strip().lower(),
            'created_at': get_current_timestamp()
        }
        
        users_db.append(new_user)
        next_user_id += 1
        
        logger.info(f"Created new user: {new_user['email']}")
        
        return jsonify({
            'success': True,
            'data': new_user,
            'message': 'User created successfully',
            'timestamp': get_current_timestamp()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'timestamp': get_current_timestamp()
        }), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    try:
        user = find_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': f'User with ID {user_id} not found',
                'timestamp': get_current_timestamp()
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided',
                'timestamp': get_current_timestamp()
            }), 400
        
        # Update user fields
        if 'name' in data and data['name'].strip():
            user['name'] = data['name'].strip()
        
        if 'email' in data and data['email'].strip():
            # Check for duplicate email
            existing_user = next((u for u in users_db if u['email'].lower() == data['email'].lower() and u['id'] != user_id), None)
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': 'User with this email already exists',
                    'timestamp': get_current_timestamp()
                }), 409
            user['email'] = data['email'].strip().lower()
        
        if 'role' in data:
            user['role'] = data['role'].strip().lower()
        
        user['updated_at'] = get_current_timestamp()
        
        logger.info(f"Updated user: {user['email']}")
        
        return jsonify({
            'success': True,
            'data': user,
            'message': 'User updated successfully',
            'timestamp': get_current_timestamp()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'timestamp': get_current_timestamp()
        }), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        user = find_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': f'User with ID {user_id} not found',
                'timestamp': get_current_timestamp()
            }), 404
        
        users_db.remove(user)
        
        logger.info(f"Deleted user: {user['email']}")
        
        return jsonify({
            'success': True,
            'message': f'User {user_id} deleted successfully',
            'timestamp': get_current_timestamp()
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'timestamp': get_current_timestamp()
        }), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': get_current_timestamp()
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'timestamp': get_current_timestamp()
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': get_current_timestamp()
    }), 500

# Main execution
if __name__ == '__main__':
    logger.info("Starting Backend API Server...")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    logger.info(f"Host: {app.config['HOST']}")
    logger.info(f"Port: {app.config['PORT']}")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )