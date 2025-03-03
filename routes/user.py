from flask import Blueprint, jsonify, make_response, redirect, render_template, request, session, url_for

from models.post import Post
from models.user import User
from models import db

from utils import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/me', methods=['GET', 'DELETE'])
@token_required
def current_user(user_id):
    
    user = User.query.filter_by(id=user_id).first()
    
    if request.method == 'GET':
        return jsonify({
            'user_id': user.id,
            'username': user.username
        }), 200
    
    elif request.method == 'DELETE':
        
        db.session.delete(user)
        db.session.commit()

        response = make_response(jsonify({"message": "Conta excluída com sucesso"}))
        response.delete_cookie("token")
        session.clear()
        return response
    
@user_bp.route('/posts')
@token_required
def get_user_posts(user_id):
    
    posts = Post.query.filter_by(user_id=user_id).all()
    return jsonify({
        'success': True,
        'posts': Post.serialize_list(posts)
    }), 200
