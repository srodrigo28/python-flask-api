from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Loja, Produto

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/', methods=['POST'])
@jwt_required()
def add_produto():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validação de dados
    name = data.get('name')
    price = data.get('price')
    description = data.get('description', '')
    stock = data.get('stock', 0)
    image_url = data.get('image_url', '')

    if not name or price is None:
        return jsonify({"error": "Nome e preço são obrigatórios"}), 400

    # Verifica se o usuário tem uma loja
    loja = Loja.query.filter_by(user_id=current_user_id).first()
    
    if not loja:
        return jsonify({"error": "Você precisa criar uma loja antes de adicionar produtos."}), 403

    novo_produto = Produto(
        name=name,
        price=price,
        description=description,
        stock=stock,
        image_url=image_url,
        loja_id=loja.id
    )

    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({"message": "Produto adicionado com sucesso!", "produto_id": novo_produto.id}), 201

@produtos_bp.route('/', methods=['GET'])
@jwt_required()
def get_meus_produtos():
    current_user_id = get_jwt_identity()
    
    loja = Loja.query.filter_by(user_id=current_user_id).first()
    if not loja:
         return jsonify({"error": "Loja não encontrada."}), 404

    produtos = Produto.query.filter_by(loja_id=loja.id).all()
    
    produtos_data = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "stock": p.stock,
        "image_url": p.image_url
    } for p in produtos]

    return jsonify(produtos_data), 200
