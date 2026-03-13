from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Loja, Produto
from slugify import slugify

lojas_bp = Blueprint('lojas', __name__)

@lojas_bp.route('/', methods=['POST'])
@jwt_required()
def create_loja():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description', '')

    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({"error": "O nome da loja é obrigatório"}), 400

    name = name.strip()
    if len(name) < 3:
         return jsonify({"error": "O nome da loja deve ter pelo menos 3 caracteres"}), 400

    slug = slugify(name)
    
    # Verifica se já existe uma loja com esse slug
    if Loja.query.filter_by(slug=slug).first():
        return jsonify({"error": "Já existe uma loja com este nome/slug"}), 400

    new_loja = Loja(name=name, slug=slug, description=description, user_id=current_user_id)
    db.session.add(new_loja)
    db.session.commit()

    return jsonify({"message": "Loja criada com sucesso!", "slug": slug}), 201

@lojas_bp.route('/<slug>', methods=['GET'])
def get_loja(slug):
    loja = Loja.query.filter_by(slug=slug).first()
    
    if not loja:
        return jsonify({"error": "Loja não encontrada"}), 404
        
    # Obtém produtos da loja
    produtos = Produto.query.filter_by(loja_id=loja.id).all()
    produtos_data = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "stock": p.stock,
        "image_url": p.image_url
    } for p in produtos]

    return jsonify({
        "id": loja.id,
        "name": loja.name,
        "description": loja.description,
        "plan_type": loja.plan_type,
        "created_at": loja.created_at,
        "produtos": produtos_data
    }), 200

@lojas_bp.route('/upgrade', methods=['POST'])
@jwt_required()
def upgrade_plan():
    current_user_id = get_jwt_identity()
    loja = Loja.query.filter_by(user_id=current_user_id).first()
    
    if not loja:
        return jsonify({"error": "Você não possui uma loja para atualizar."}), 404
        
    # Na vida real aqui haveria integração com Stripe/MercadoPago
    if loja.plan_type == 'pro':
        return jsonify({"message": "Sua loja já está no plano Pro!"}), 200
        
    loja.plan_type = 'pro'
    db.session.commit()
    
    return jsonify({"message": "Updrade para o plano Pro realizado com sucesso!"}), 200
