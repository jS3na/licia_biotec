from functools import wraps
from flask import jsonify, request
import jwt
from config import ApplicationConfig

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = request.cookies.get('token')
        
        # if not token:
        #     return jsonify({"error": "Sem usuário logado"}), 401
        
        # try:
        #     data = jwt.decode(token, ApplicationConfig.SECRET_KEY, algorithms=["HS256"])
        #     user_id = data['user_id']
        # except jwt.ExpiredSignatureError:
        #     return jsonify({"error": "Sem usuário logado"}), 401
        # except jwt.InvalidTokenError:
        #     return jsonify({"error": "Sem usuário logado"}), 401
        
        return f(user_id=1, *args, **kwargs)
    
    return decorated

def logout_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            return f(*args, **kwargs)
        
        try:
            data = jwt.decode(token, ApplicationConfig.SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return f(*args, **kwargs)
        except jwt.InvalidTokenError:
            return f(*args, **kwargs)
        
        return jsonify({'error': 'Logout required'}), 403
    
    return decorated
