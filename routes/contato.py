from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from flask_mail import Message

from extensions import mail
from config import ApplicationConfig

contato_bp = Blueprint('contato', __name__)
        
@contato_bp.route('/', methods=['POST'])
def handle_email_send():
    
    data = request.json
    
    nome = data.get('nome')
    email = data.get('email')
    descricao = data.get('descricao')
    
    msg = Message(subject='Solicitação de Contato / Sugestão / Elogio', sender=ApplicationConfig.MAIL_USERNAME, recipients=[ApplicationConfig.MAIL_USERNAME])
    msg.body = f"{nome} - {email} - {descricao}"
    mail.send(msg)

    return jsonify({
        'success': True,
        'message': 'Contato Enviado',
    }), 200
