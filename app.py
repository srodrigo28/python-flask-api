from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app) # Permite comunicação com o front-end (Next.js)

    # Configurações do Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Importar models
    from models import db, migrate

    # Inicializa os plugins (Banco de Dados e Migrations)
    db.init_app(app)
    migrate.init_app(app, db)
    
    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    # Importar rotas
    from routes.auth import auth_bp
    from routes.lojas import lojas_bp
    from routes.produtos import produtos_bp
    from routes.master import master_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(lojas_bp, url_prefix='/api/lojas')
    app.register_blueprint(produtos_bp, url_prefix='/api/admin/produtos')
    app.register_blueprint(master_bp, url_prefix='/api/master')

    @app.route('/')
    def index():
        return jsonify({
            "message": "API Flask Mult-loja Online!",
            "routes_map": {
                "auth": {
                    "POST /api/auth/register": "Cadastra um novo usuário dono de loja",
                    "POST /api/auth/login": "Login e geração de token JWT"
                },
                "loja_tenants": {
                    "POST /api/lojas/": "Cria uma nova loja vinculada ao usuário logado",
                    "GET /api/lojas/<slug>": "Visualiza dados públicos da loja e seus produtos"
                },
                "produtos_dono": {
                    "POST /api/admin/produtos/": "Adiciona um novo produto na loja do usuário",
                    "GET /api/admin/produtos/": "Lista os produtos da loja do usuário logado"
                },
                "painel_master": {
                    "GET /api/master/lojas": "Lista todas as lojas cadastradas no sistema",
                    "GET /api/master/estatisticas": "Métricas de usuários, lojas, produtos e crescimento"
                }
            }
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
