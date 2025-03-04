from sqlalchemy import func
from models import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imagem_url = db.Column(db.Text, nullable=False)
    setor = db.Column(db.String(200), nullable=False)
    achado = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    curtidas = db.Column(db.Integer, nullable=False, default=0)
    comentarios = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    
    _user = db.relationship('User', back_populates='_posts', lazy='joined')
    _curtidas = db.relationship('Curtida', back_populates='_post', cascade="all, delete-orphan")
    _comentarios = db.relationship('Comentario', back_populates='_post', cascade="all, delete-orphan")
    
    def serializer(self):
        return {
            'id': self.id,
            'imagem_url': self.imagem_url,
            'setor': self.setor,
            'achado': self.achado,
            'descricao': self.descricao,
            'curtidas': self.curtidas,
            'comentarios': self.comentarios,
            'user_id': self.user_id,
            'user': self._user.username,
            'criado_em': self.criado_em
        }

    @staticmethod
    def serialize_list(posts):
        return [post.serializer() for post in posts]