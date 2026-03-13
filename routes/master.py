from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Loja, User, Produto

master_bp = Blueprint('master', __name__)

@master_bp.route('/lojas', methods=['GET'])
@jwt_required()
def listar_todas_lojas():
    # Em um cenário real, você verificaria se get_jwt_identity() pertence a um admin master
    # Ex: user = User.query.get(get_jwt_identity()); if not user.is_admin: return 403
    
    lojas = Loja.query.all()
    lojas_data = []

    for loja in lojas:
        dono = User.query.get(loja.user_id)
        lojas_data.append({
            "id": loja.id,
            "name": loja.name,
            "slug": loja.slug,
            "description": loja.description,
            "dono_nome": dono.name if dono else "Desconhecido",
            "dono_email": dono.email if dono else "Desconhecido",
            "created_at": loja.created_at
        })

    return jsonify(lojas_data), 200

@master_bp.route('/estatisticas', methods=['GET'])
@jwt_required()
def obter_estatisticas():
    # Validação fictícia de Admin Master (recomenda-se adicionar campo is_admin no model User)
    
    total_lojas = Loja.query.count()
    total_produtos = Produto.query.count()
    total_usuarios = User.query.count()
    
    # Contagem de produtos por loja
    lojas = Loja.query.all()
    produtos_por_loja = []
    
    for loja in lojas:
        qtd_produtos = Produto.query.filter_by(loja_id=loja.id).count()
        produtos_por_loja.append({
            "loja_nome": loja.name,
            "quantidade_produtos": qtd_produtos
        })
        
    # Ordenar pelas lojas que têm mais produtos (Top 5)
    top_lojas = sorted(produtos_por_loja, key=lambda x: x['quantidade_produtos'], reverse=True)[:5]
    
    # Crescimento: Quantos usuários cadastrados nos últimos 7 dias
    from datetime import datetime, timedelta
    sete_dias_atras = datetime.utcnow() - timedelta(days=7)
    novos_usuarios_semana = User.query.filter(User.created_at >= sete_dias_atras).count()
    novas_lojas_semana = Loja.query.filter(Loja.created_at >= sete_dias_atras).count()

    estatisticas = {
        "geral": {
            "total_usuarios": total_usuarios,
            "total_lojas": total_lojas,
            "total_produtos": total_produtos,
        },
        "crescimento_ultima_semana": {
            "novos_usuarios": novos_usuarios_semana,
            "novas_lojas": novas_lojas_semana
        },
        "top_lojas_com_mais_produtos": top_lojas,
        "detalhamento_produtos_por_loja": produtos_por_loja
    }

    return jsonify(estatisticas), 200
