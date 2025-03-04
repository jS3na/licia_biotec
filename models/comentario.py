from sqlalchemy import func
from models import db

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=func.now())
    
    _post = db.relationship('Post', back_populates='_comentarios', lazy='joined')
    _user = db.relationship('User', back_populates='_comentarios', lazy='joined')
    
    def serializer(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'comentario': self.comentario,
            'criado_em': self.criado_em,
            'user': self._user.username
        }
        
    @staticmethod
    def serialize_list(comentarios):
        return [comentario.serializer() for comentario in comentarios]
