from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from models.post import Post
from models.comentario import Comentario

from utils import token_required

from models import db

comentario_bp = Blueprint('comentario', __name__)

@comentario_bp.route('/<int:post_id>', methods=['GET'])
def get_post_comentarios(post_id):
    
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        return jsonify({
            'error': 'Post não encontrado'
        }), 404
        
    comentarios = Comentario.query.filter_by(post_id=post_id).all()
    
    return jsonify({
        'success': True,
        'comentarios': Comentario.serialize_list(comentarios)
    }), 200
        
@comentario_bp.route('/create/<int:post_id>', methods=['POST'])
@token_required
def create_post_comentario(post_id, user_id):
    
        data = request.json
        comentario = data.get('comentario')
        
        if not comentario:
            return jsonify({"error": "Comentário não pode ser vazio"}), 400
        
        post = Post.query.filter_by(id=post_id).first()
        
        if not post:
            return jsonify({"error": "Post não encontrado"}), 404
        
        comentario = Comentario(
            comentario=comentario,
            post_id=post_id,
            user_id=user_id
        )
        
        db.session.add(comentario)
        
        post.comentarios = post.comentarios + 1
        
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Comentário adicionado com sucesso',
            'comentario': Comentario.serializer(comentario)
        }), 200
        
@comentario_bp.route('/<int:comentario_id>', methods=['DELETE'])
@token_required
def delete_comentario(comentario_id, user_id):
    
    comentario = Comentario.query.filter_by(id=comentario_id, user_id=user_id).first()
    
    if not comentario:
        return jsonify({
            'error': 'Comentário não encontrado'
        }), 404
    
    post = Post.query.filter_by(id=comentario.post_id).first()

    if request.method == 'DELETE':
        db.session.delete(comentario)
        post.comentarios = post.comentarios - 1
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Comentário deletado com sucesso'
        }), 200
    
