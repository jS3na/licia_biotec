from flask import Blueprint, make_response, request, session, jsonify
from models.user import User
from models import db
import jwt
import datetime
from config import ApplicationConfig
from utils import logout_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@logout_required
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    
    user = User.query.filter_by(email=email).first()

    if user and user.check_senha(senha):
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, ApplicationConfig.SECRET_KEY)

        response = make_response(jsonify({
            "success": True,
            "message": 'Login bem-sucedido!'
        }))
        
        response.set_cookie('token', token, httponly=True, secure=True, max_age=datetime.timedelta(minutes=30), samesite='None')

        return response
    
    return jsonify({"error": "Credenciais Inválidas"}), 401

@auth_bp.route('/registro', methods=['POST'])
@logout_required
def registro():
    data = request.json
    email = data.get('email')
    nome = data.get('nome')
    sobrenome = data.get('sobrenome', '')
    username = data.get('username')
    senha = data.get('senha')
    graduacao = data.get('graduacao')
    status = data.get('status')
    estado = data.get('estado')
    cidade = data.get('cidade')
    admin = 0

    if not all([email, nome, username, senha, graduacao, status, estado, cidade]):
        return jsonify({"error": "Preencha os campos obrigatórios"}), 400

    existing_user_email = User.query.filter_by(email=email).first()
    existing_user_username = User.query.filter_by(username=username).first()

    if existing_user_email or existing_user_username:
        return jsonify({"error": "Já existe um usuário com esse email ou nome de usuário"}), 400

    user = User(
        email=email,
        nome=nome + ' ' + sobrenome,
        username=username,
        graduacao=graduacao,
        status=status,
        estado=estado,
        cidade=cidade,
        admin=admin,
    )
    user.set_senha(senha)
    db.session.add(user)
    db.session.commit()

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, ApplicationConfig.SECRET_KEY)

    response = make_response(jsonify({
        "success": True,
        "message": "Registro realizado com sucesso"
    }))
    
    response.set_cookie('token', token, httponly=True, secure=True, max_age=datetime.timedelta(minutes=30), samesite='Lax')

    return response


@auth_bp.route('/logout')
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    response.delete_cookie("token")
    session.clear()
    return response
