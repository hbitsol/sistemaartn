from flask import Blueprint, request, jsonify
from decimal import Decimal, InvalidOperation
from pathlib import Path
import json

from src.models.user import db
from src.models.material import Material
from src.models.difficulty import DifficultyFactor
from src.models.project import Project, ProjectItem
from src.models.client import Client

pricing_bp = Blueprint("pricing", __name__)  # mantém sem url_prefix para não quebrar quem registra


# ---------- Utilidades ----------

DATA_PATH = (Path(__file__).resolve().parents[1] / "extracted_pricing_data.json")

def load_pricing_data():
    """
    Carrega o JSON de regras a partir de src/extracted_pricing_data.json.
    Não levanta exceção para não derrubar o servidor; retorna dict com 'error' em caso de problema.
    """
    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"file not found: {DATA_PATH.name}", "rules": []}
    except json.JSONDecodeError as e:
        return {"error": f"invalid JSON in {DATA_PATH.name}: {e}", "rules": []}
    except Exception as e:
        return {"error": f"failed to load {DATA_PATH.name}: {e}", "rules": []}

def to_decimal(value, field_name):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"Invalid decimal value for '{field_name}': {value!r}")

def require_fields(payload, fields):
    for f in fields:
        if f not in payload:
            raise KeyError(f"Missing required field: {f}")


# ---------- Endpoints ----------

@pricing_bp.route("/materials", methods=["GET"])
def get_materials():
    """Get all available materials"""
    try:
        materials = Material.query.all()
        return jsonify([m.to_dict() for m in materials])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pricing_bp.route("/difficulty-factors", methods=["GET"])
def get_difficulty_factors():
    """Get all difficulty factors"""
    try:
        factors = DifficultyFactor.query.all()
        return jsonify([f.to_dict() for f in factors])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pricing_bp.route("/calculate-price", methods=["POST"])
def calculate_price():
    """Calculate price for a single item"""
    try:
        data = request.get_json(force=True, silent=False) or {}
        require_fields(data, ["material_id", "quantity", "difficulty_id", "employee_level", "estimated_days", "num_envelopers"])

        # Carrega regras
        rules = load_pricing_data()
        if "error" in rules:
            return jsonify({"error": rules["error"]}), 500

        material = Material.query.get(data["material_id"])
        if not material:
            return jsonify({"error": "Material not found"}), 404

        difficulty_factor_obj = DifficultyFactor.query.get(data["difficulty_id"])
        if not difficulty_factor_obj:
            return jsonify({"error": "Difficulty factor not found"}), 404

        employee_level = data["employee_level"]
        employee_rates = rules.get("employee_rates", {})
        if employee_level not in employee_rates:
            return jsonify({"error": "Invalid employee level"}), 400

        # Difficulty data por nível
        diff_all = rules.get("difficulty_factors", {})
        difficulty_data = diff_all.get(difficulty_factor_obj.nivel)
        if not difficulty_data:
            return jsonify({"error": "Difficulty data not found for selected level"}), 400

        # Conversões seguras
        quantity = to_decimal(data["quantity"], "quantity")
        estimated_days = to_decimal(data["estimated_days"], "estimated_days")
        num_envelopers = to_decimal(data["num_envelopers"], "num_envelopers")

        material_multiplier = to_decimal(difficulty_data.get("material_multiplier", "1"), "material_multiplier")
        tax_rate = to_decimal(difficulty_data.get("tax_rate", "0"), "tax_rate")

        # Custos
        material_cost = quantity * Decimal(str(material.custo_unitario_base)) * material_multiplier
        daily_rate = to_decimal(employee_rates[employee_level], "employee_rates[employee_level]")
        labor_cost = daily_rate * estimated_days * num_envelopers
        total_cost_before_tax = material_cost + labor_cost
        total_cost = total_cost_before_tax * (Decimal("1") + tax_rate)

        # Margem
        margin_ranges = rules.get("margin_ranges", {})
        margin = to_decimal(margin_ranges.get("min", "0"), "margin_ranges.min")
        selling_price = total_cost * (Decimal("1") + margin)

        result = {
            "material_cost": float(material_cost),
            "labor_cost": float(labor_cost),
            "total_cost_before_tax": float(total_cost_before_tax),
            "tax_rate_applied": float(tax_rate),
            "total_cost": float(total_cost),
            "margin_applied": float(margin),
            "selling_price": float(selling_price),
            "material": material.to_dict(),
            "difficulty": difficulty_factor_obj.to_dict(),
            "employee_level": employee_level,
            "estimated_days": float(estimated_days),
            "num_envelopers": float(num_envelopers),
        }
        return jsonify(result)

    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@pricing_bp.route("/projects", methods=["POST"])
def create_project():
    """Create a new project with items"""
    try:
        payload = request.get_json(force=True, silent=False) or {}
        require_fields(payload, ["nome_projeto", "id_cliente", "id_franqueado", "items"])

        rules = load_pricing_data()
        if "error" in rules:
            return jsonify({"error": rules["error"]}), 500

        margin_default = to_decimal(rules.get("margin_ranges", {}).get("min", "0"), "margin_ranges.min")

        project = Project(
            nome_projeto=payload["nome_projeto"],
            id_cliente=payload["id_cliente"],
            id_franqueado=payload["id_franqueado"],
            margem_lucro_aplicada=to_decimal(payload.get("margem_lucro", margin_default), "margem_lucro")
        )

        db.session.add(project)
        db.session.flush()  # garante project.id

        total_cost = Decimal("0")
        total_selling_price = Decimal("0")

        employee_rates = rules.get("employee_rates", {})
        diff_all = rules.get("difficulty_factors", {})

        for item in payload["items"]:
            require_fields(item, ["material_id", "quantity", "difficulty_id", "employee_level", "estimated_days", "num_envelopers"])

            material = Material.query.get(item["material_id"])
            if not material:
                return jsonify({"error": f"Material not found: {item['material_id']}"}), 404

            difficulty_factor_obj = DifficultyFactor.query.get(item["difficulty_id"])
            if not difficulty_factor_obj:
                return jsonify({"error": f"Difficulty factor not found: {item['difficulty_id']}"}), 404

            employee_level = item["employee_level"]
            if employee_level not in employee_rates:
                return jsonify({"error": f"Invalid employee level: {employee_level}"}), 400

            difficulty_data = diff_all.get(difficulty_factor_obj.nivel)
            if not difficulty_data:
                return jsonify({"error": f"Difficulty data not found for level: {difficulty_factor_obj.nivel}"}), 400

            quantity = to_decimal(item["quantity"], "items[].quantity")
            estimated_days = to_decimal(item["estimated_days"], "items[].estimated_days")
            num_envelopers = to_decimal(item["num_envelopers"], "items[].num_envelopers")
            material_multiplier = to_decimal(difficulty_data.get("material_multiplier", "1"), "material_multiplier")
            tax_rate = to_decimal(difficulty_data.get("tax_rate", "0"), "tax_rate")
            daily_rate = to_decimal(employee_rates[employee_level], "employee_rates[level]")

            material_cost = quantity * Decimal(str(material.custo_unitario_base)) * material_multiplier
            labor_cost = daily_rate * estimated_days * num_envelopers
            item_cost_before_tax = material_cost + labor_cost
            item_cost = item_cost_before_tax * (Decimal("1") + tax_rate)
            item_selling_price = item_cost * (Decimal("1") + project.margem_lucro_aplicada)

            project_item = ProjectItem(
                id_projeto=project.id,
                id_material=item["material_id"],
                quantidade=quantity,
                id_dificuldade=item["difficulty_id"],
                custo_item=item_cost,
                preco_venda_item=item_selling_price,
                observacoes=item.get("observacoes", "")
            )
            db.session.add(project_item)

            total_cost += item_cost
            total_selling_price += item_selling_price

        project.custo_total_estimado = total_cost
        project.preco_venda_sugerido = total_selling_price

        db.session.commit()

        return jsonify({"project": project.to_dict(), "message": "Project created successfully"}), 201

    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@pricing_bp.route("/projects/<project_id>", methods=["GET"])
def get_project(project_id):
    """Get project details with items"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404

        project_data = project.to_dict()
        project_data["items"] = [item.to_dict() for item in project.items]
        return jsonify(project_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500