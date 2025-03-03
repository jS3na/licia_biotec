from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from models.post import Post
from models.curtida import Curtida

from utils import token_required

from models import db

curtida_bp = Blueprint('curtida', __name__)
        
@curtida_bp.route('/<int:post_id>', methods=['POST', 'DELETE'])
@token_required
def handle_post_curtida(post_id, user_id):
    
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        return jsonify({
            'error': 'Post não encontrado'
        }), 404

    if request.method == 'POST':
        
        curtida = Curtida(
            post_id=post_id,
            user_id=user_id
        )
        
        db.session.add(curtida)
        post.curtidas = post.curtidas + 1
        
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Curtida adicionada com sucesso',
        }), 200
        
    elif request.method == 'DELETE':
        
        curtida = Curtida.query.filter_by(post_id=post_id, user_id=user_id).first()
        db.session.delete(curtida)
        post.curtidas = post.curtidas - 1
        
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Curtida deletada com sucesso'
        }), 200
        
    
