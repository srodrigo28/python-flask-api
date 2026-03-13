from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento 1:N com as lojas (Um usuário pode ter muitas lojas)
    lojas = db.relationship('Loja', backref='dono', lazy=True)

class Loja(db.Model):
    __tablename__ = 'lojas'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # FK para o User (dono da loja)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamento 1:N com os produtos
    produtos = db.relationship('Produto', backref='loja', lazy=True)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # FK para a loja
    loja_id = db.Column(db.String(36), db.ForeignKey('lojas.id'), nullable=False)
