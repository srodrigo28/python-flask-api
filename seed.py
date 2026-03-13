import sys
from app import create_app
from models import db, User, Loja, Produto
from werkzeug.security import generate_password_hash
import random

def run_seed():
    app = create_app()
    with app.app_context():
        # First ensure tables are created
        db.create_all()

        # Check if the database is already seeded to avoid duplication
        if User.query.filter_by(email="admin@lojas.com").first():
            print("Banco de dados já contém o admin. Use o Flask-Migrate ou apague o banco para recriar.")
            # We can optionally drop and recreate, but dropping automatically could be dangerous.
            print("Apagando todos os dados recriando as lojas para teste...")
            db.drop_all()
            db.create_all()

        print("Criando admin e 10 lojas de teste...")

        # Create Master Admin user
        admin = User(name='Admin Master', email='admin@lojas.com', password=generate_password_hash('123456'))
        db.session.add(admin)
        db.session.commit()

        lojas_data = [
            {"name": "Tech Store", "slug": "tech-store", "desc": "Os melhores eletrônicos e gadgets."},
            {"name": "Moda Fashion", "slug": "moda-fashion", "desc": "Roupas e tendências da moda."},
            {"name": "Mundo dos Esportes", "slug": "mundo-esportes", "desc": "Tudo para o seu treino."},
            {"name": "Livraria Saber", "slug": "livraria-saber", "desc": "Livros de diversos gêneros."},
            {"name": "Gourmet Foods", "slug": "gourmet-foods", "desc": "Lanches deliciosos e diferenciados."},
            {"name": "Casa & Conforto", "slug": "casa-conforto", "desc": "Decoração e itens para casa."},
            {"name": "Brinquedos Kids", "slug": "brinquedos-kids", "desc": "Alegria e diversão garantida."},
            {"name": "Beleza Plus", "slug": "beleza-plus", "desc": "Cosméticos e cuidados de beleza."},
            {"name": "Som & Música", "slug": "som-musica", "desc": "Instrumentos e acessórios de áudio."},
            {"name": "Pet Paradise", "slug": "pet-paradise", "desc": "Tudo o que seu pet precisa."}
        ]

        for i, data in enumerate(lojas_data):
            # Create a store owner user
            user = User(
                name=f'Dono {data["name"]}', 
                email=f'dono{i+1}@loja.com', 
                password=generate_password_hash('123456')
            )
            db.session.add(user)
            db.session.commit()

            # Determine se a loja será free ou pro para fins de teste
            plan = 'pro' if i % 2 == 0 else 'free'
            
            # Create the store
            loja = Loja(
                name=data["name"], 
                slug=data["slug"], 
                description=data["desc"], 
                plan_type=plan,
                user_id=user.id
            )
            db.session.add(loja)
            db.session.commit()

            # Create 5 products for each store
            for j in range(5):
                produto = Produto(
                    name=f'Produto {(j+1):02d} da {data["name"]}',
                    description=f'Descrição super detalhada do produto {(j+1):02d}. Ideal para qualquer ocasião.',
                    price=round(random.uniform(20.0, 999.99), 2),
                    stock=random.randint(5, 100),
                    image_url=f"https://placehold.co/400x400/png?text=Prod+{(j+1)}",
                    loja_id=loja.id
                )
                db.session.add(produto)
            
            db.session.commit()
            print(f"- Loja Criada: {data['name']} (Plano: {plan.upper()}) com Dono: dono{i+1}@loja.com")

        print("===============================================")
        print("SEED REALIZADO COM SUCESSO!")
        print("-> 1 Admin Master (admin@lojas.com)")
        print("-> 10 Lojas com donos (Plano misto Free/Pro)")
        print("-> 50 Produtos criados (5 por loja)")
        print("A senha para todos os usuários é: 123456")
        print("===============================================")

if __name__ == '__main__':
    try:
        run_seed()
    except Exception as e:
        print(f"Erro ao executar seed: {e}")
