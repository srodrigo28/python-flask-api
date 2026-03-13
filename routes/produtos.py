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

    # Verifica o limite do plano SaaS (Free = máx 20 produtos)
    if loja.plan_type == 'free':
        count_produtos = Produto.query.filter_by(loja_id=loja.id).count()
        if count_produtos >= 20:
            return jsonify({
                "error": "Limite de produtos atingido.",
                "message": "Seu plano Free permite apenas 20 produtos. Faça o upgrade para o plano Pro para cadastrar produtos ilimitados!"
            }), 403

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

@produtos_bp.route('/<produto_id>', methods=['GET'])
@jwt_required()
def get_produto(produto_id):
    current_user_id = get_jwt_identity()
    loja = Loja.query.filter_by(user_id=current_user_id).first()
    
    if not loja:
        return jsonify({"error": "Loja não encontrada."}), 404

    produto = Produto.query.filter_by(id=produto_id, loja_id=loja.id).first()
    
    if not produto:
        return jsonify({"error": "Produto não encontrado ou não pertence a esta loja."}), 404

    return jsonify({
        "id": produto.id,
        "name": produto.name,
        "description": produto.description,
        "price": produto.price,
        "stock": produto.stock,
        "image_url": produto.image_url
    }), 200

@produtos_bp.route('/<produto_id>', methods=['PUT'])
@jwt_required()
def update_produto(produto_id):
    current_user_id = get_jwt_identity()
    loja = Loja.query.filter_by(user_id=current_user_id).first()
    
    if not loja:
        return jsonify({"error": "Loja não encontrada."}), 404

    produto = Produto.query.filter_by(id=produto_id, loja_id=loja.id).first()
    
    if not produto:
        return jsonify({"error": "Produto não encontrado ou não pertence a esta loja."}), 404

    data = request.get_json()
    
    # Atualiza apenas os campos enviados
    if 'name' in data:
        produto.name = data['name']
    if 'price' in data:
        produto.price = data['price']
    if 'description' in data:
        produto.description = data['description']
    if 'stock' in data:
        produto.stock = data['stock']
    if 'image_url' in data:
        produto.image_url = data['image_url']

    db.session.commit()

    return jsonify({"message": "Produto atualizado com sucesso!"}), 200

@produtos_bp.route('/<produto_id>', methods=['DELETE'])
@jwt_required()
def delete_produto(produto_id):
    current_user_id = get_jwt_identity()
    loja = Loja.query.filter_by(user_id=current_user_id).first()
    
    if not loja:
        return jsonify({"error": "Loja não encontrada."}), 404

    produto = Produto.query.filter_by(id=produto_id, loja_id=loja.id).first()
    
    if not produto:
        return jsonify({"error": "Produto não encontrado ou não pertence a esta loja."}), 404

    db.session.delete(produto)
    db.session.commit()

    return jsonify({"message": "Produto excluído com sucesso!"}), 200
