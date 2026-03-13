from app import create_app
from models import db
from flask_migrate import upgrade, migrate, init

import os

app = create_app()

with app.app_context():
    if not os.path.exists('migrations'):
        try:
            init()
            print("Migrações inicializadas.")
        except Exception as e:
            print("Init já foi rodado ou erro:", e)
    else:
        print("Pasta migrations já existe, pulando init.")

    try:
        migrate(message="Initial migration")
        print("Migração criada.")
    except Exception as e:
        print("Erro ao criar migração:", e)
        
    try:
        upgrade()
        print("Banco de dados atualizado.")
    except Exception as e:
        print("Erro no upgrade do banco:", e)
