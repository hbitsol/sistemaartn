from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from typing import Optional

from src.models.user import db
from src.models.material import Material
from src.models.difficulty import DifficultyFactor
from src.models.client import Client
from src.models.project import Project
from src.models.franchise import Franchise

seed_bp = Blueprint("seed", __name__)

def get_or_create(model, defaults: Optional[dict] = None, **kwargs):
    inst = model.query.filter_by(**kwargs).first()
    if inst:
        if defaults:
            for k, v in defaults.items():
                setattr(inst, k, v)
        return inst, False
    params = dict(kwargs)
    if defaults:
        params.update(defaults)
    inst = model(**params)
    db.session.add(inst)
    return inst, True

# --------- seeds ---------
DEFAULT_FRANCHISE = {
    "nome_franquia": "Artn Master",
    "cnpj": "42224833000186",
    "endereco": "Rua das Esmeraldas, 395, 12 andar, Bairro Jardim, Santo André, São Paulo, 09090-070",
    "telefone": "11989295491",
}

MATERIALS = [
    ("Alltak Premium",        "m²", "25.00"),
    ("Alltak Decor",          "m²", "65.00"),
    ("Alltak Tunning",        "m²", "60.00"),
    ("Imprimax Linha Gold",   "m²", "65.00"),
    ("Imprimax Linha Jateado","m²", "55.00"),
    ("SH Decor",              "m²", "98.00"),
    ("SH Decor Piso",         "m²","170.00"),
    ("PPF SH",                "m²","180.00"),
]

DIFFICULTIES = [
    ("1", "Baixa complexidade", "1.0"),
    ("2", "Média complexidade", "1.2"),
    ("3", "Alta complexidade",  "1.5"),
]

CLIENTS = [
    ("Cliente Demo A", "clienteA@example.com"),
    ("Cliente Demo B", "clienteB@example.com"),
]

@seed_bp.post("/seed")
def seed_all():
    try:
        created = {"franchises": 0, "materials": 0, "difficulties": 0, "clients": 0}

        # 1) Franquia default
        fr, is_new_fr = get_or_create(
            Franchise,
            defaults={
                "cnpj": DEFAULT_FRANCHISE["cnpj"],
                "endereco": DEFAULT_FRANCHISE["endereco"],
                "telefone": DEFAULT_FRANCHISE["telefone"],
            },
            nome_franquia=DEFAULT_FRANCHISE["nome_franquia"],
        )
        if is_new_fr:
            created["franchises"] += 1

        # 2) Materiais
        for nome, unidade, unit_cost in MATERIALS:
            _, is_new = get_or_create(
                Material,
                defaults={
                    "unidade_medida": unidade,
                    "custo_unitario_base": Decimal(unit_cost),
                },
                nome=nome,
            )
            if is_new:
                created["materials"] += 1

        # 3) Dificuldades
        for nivel, descricao, fator in DIFFICULTIES:
            _, is_new = get_or_create(
                DifficultyFactor,
                defaults={
                    "descricao": descricao,
                    "fator_multiplicador_mao_obra": Decimal(fator),
                },
                nivel=nivel,
            )
            if is_new:
                created["difficulties"] += 1

        # 4) Clientes → todos atrelados à franquia default
        for nome, email in CLIENTS:
            _, is_new = get_or_create(
                Client,
                defaults={
                    "email": email,
                    "id_franqueado": fr.id,   # <- agora aponta para franchises.id
                },
                nome=nome,
            )
            if is_new:
                created["clients"] += 1

        db.session.commit()
        return jsonify({"status": "ok", "created": created}), 201

    except IntegrityError as ie:
        db.session.rollback()
        return jsonify({"error": f"Integrity error: {ie}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@seed_bp.get("/seed/check")
def seed_check():
    try:
        return jsonify({
            "franchises": Franchise.query.count(),
            "materials": Material.query.count(),
            "difficulties": DifficultyFactor.query.count(),
            "clients": Client.query.count(),
            "projects": Project.query.count(),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500