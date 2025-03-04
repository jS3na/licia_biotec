from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
import jwt

from config import ApplicationConfig
from models.post import Post
from models.curtida import Curtida
from models.comentario import Comentario

from utils import token_required, verify_login

from models import db

post_bp = Blueprint('post', __name__)

@post_bp.route('/', methods=['GET'])
@verify_login
def handle_posts(user_id):
    if request.method == 'GET':
        posts = Post.query.order_by(Post.criado_em.desc())
        
        print(user_id)
        
        posts_data = []
        for post in posts:
            user_curtida = Curtida.query.filter_by(post_id=post.id, user_id=user_id).first() if user_id else None
            post_data = Post.serializer(post)
            post_data['curtido'] = user_curtida is not None
            
            posts_data.append(post_data)

        return jsonify({
            'success': True,
            'posts': posts_data,
            'user_id': user_id
        }), 200

@post_bp.route('/create', methods=['POST'])
@token_required
def handle_create_posts(user_id):
    data = request.json
    
    imagem_url = data.get('imagem_url')
    setor = data.get('setor')
    achado = data.get('achado')
    descricao = data.get('descricao')
    user_id = user_id
    
    if not all([imagem_url, setor, achado, descricao]):
        return jsonify({"error": "Preencha os campos obrigatórios"}), 400
    
    post = Post(
        imagem_url=imagem_url,
        setor=setor,
        achado=achado,
        descricao=descricao,
        user_id=user_id,
    )
    
    db.session.add(post)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Post adicionado com sucesso',
        'post': Post.serializer(post)
    }), 200
    
    
@post_bp.route('/<int:post_id>', methods=['GET'])
@verify_login
def get_post(post_id, user_id):
    
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        return jsonify({
            'error': 'Post não encontrado'
        }), 404
        
    user_curtida = Curtida.query.filter_by(post_id=post.id, user_id=user_id).first() if user_id else None
    post_data = Post.serializer(post)
    post_data['curtido'] = user_curtida is not None

    return jsonify({
        'success': True,
        'post': post_data
    }), 200
        
@post_bp.route('/<int:post_id>', methods=['PUT', 'DELETE'])
@token_required
def handle_post(post_id, user_id):
    
    if request.method == 'PUT':
        data = request.json
        imagem_url = data.get('imagem_url', post.imagem_url)
        setor = data.get('setor', post.setor)
        achado = data.get('achado', post.achado)
        descricao = data.get('descricao', post.descricao)

        if not all([imagem_url, setor, achado, descricao]):
            return jsonify({"error": "Preencha os campos obrigatórios"}), 400
        
        post.imagem_url = imagem_url
        post.setor = setor
        post.achado = achado
        post.descricao = descricao

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Post atualizado com sucesso',
            'post': Post.serializer(post)
        }), 200

    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Post deletado com sucesso'
        }), 200
