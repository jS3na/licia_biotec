from bcrypt import hashpw, gensalt, checkpw
from models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    nome = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    graduacao = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(150), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    
    _posts = db.relationship('Post', back_populates='_user', cascade="all, delete-orphan")
    _curtidas = db.relationship('Curtida', back_populates='_user', cascade="all, delete-orphan")
    _comentarios = db.relationship('Comentario', back_populates='_user', cascade="all, delete-orphan")

    def set_senha(self, senha: str):
        self.senha = hashpw(senha.encode('utf-8'), gensalt()).decode('utf-8')

    def check_senha(self, senha: str) -> bool:
        return checkpw(senha.encode('utf-8'), self.senha.encode('utf-8'))
    
    def serializer(self):
        return {
            'id': self.id,
            'email': self.email,
            'nome': self.nome,
            'username': self.username,
            'graduacao': self.graduacao,
            'status': self.status,
            'estado': self.estado,
            'cidade': self.cidade,
            'admin': self.admin
        }

