from models import db

class Curtida(db.Model):
    __tablename__ = 'curtidas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    
    _post = db.relationship('Post', back_populates='_curtidas', lazy='joined')
    _user = db.relationship('User', back_populates='_curtidas', lazy='joined')
    
    def serializer(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id
        }
