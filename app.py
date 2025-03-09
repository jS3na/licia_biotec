from extensions import mail
from config import ApplicationConfig
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from routes.auth import auth_bp
from routes.user import user_bp
from routes.post import post_bp
from routes.comentario import comentario_bp
from routes.curtida import curtida_bp
from routes.contato import contato_bp

from models import db

app = Flask(__name__, static_folder='uploads')
app.config.from_object(ApplicationConfig)
mail.init_app(app)

CORS(app, supports_credentials=True, origins="*")

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(comentario_bp, url_prefix='/comentario')
app.register_blueprint(curtida_bp, url_prefix='/curtida')
app.register_blueprint(contato_bp, url_prefix='/contato')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)