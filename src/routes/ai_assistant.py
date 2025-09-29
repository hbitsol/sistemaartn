# src/routes/ai_assistant.py
from flask import Blueprint, request, jsonify
from decimal import Decimal
import json
import os

from src.models.user import db
from src.models.material import Material
from src.models.project import Project, ProjectItem
from src.models.client import Client

ai_bp = Blueprint("ai", __name__)  # mantém as rotas como estavam (sem url_prefix)


# =============== Helpers OpenAI (lazy import + compat old/new SDK) ===============

def _get_openai_client():
    """
    Tenta SDK novo (openai>=1.x) e depois o antigo (0.28.x).
    Retorna (client, mode) onde mode ∈ {"new","old"}.
    Se não houver SDK ou OPENAI_API_KEY, retorna (None, "missing").
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "missing"

    # SDK novo
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        return client, "new"
    except Exception:
        pass

    # SDK antigo
    try:
        import openai
        openai.api_key = api_key
        return openai, "old"
    except Exception:
        return None, "missing"


def _chat_complete(messages, max_tokens=500, temperature=0.7, model=None):
    """
    Faz a chamada de chat compatível com o SDK novo e antigo.
    - Usa OPENAI_MODEL (se setado) ou "gpt-4o-mini" por padrão no SDK novo.
    - No SDK antigo, cai para "gpt-3.5-turbo".
    Levanta RuntimeError se não houver SDK/chave.
    """
    client, mode = _get_openai_client()
    if client is None:
        raise RuntimeError("OpenAI SDK not installed or OPENAI_API_KEY missing")

    model = model or os.getenv("OPENAI_MODEL")
    if mode == "new":
        model = model or "gpt-4o-mini"
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content
    else:
        legacy_model = model or "gpt-3.5-turbo"
        resp = client.ChatCompletion.create(
            model=legacy_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message["content"]


def _json_from_ai(text):
    """Remove blocos ```json ... ``` se vierem e tenta fazer json.loads."""
    clean = (text or "").replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ================================ Endpoints =====================================

@ai_bp.route("/generate-project-description", methods=["POST"])
def generate_project_description():
    """Gera descrição do projeto baseada em materiais e informações do cliente."""
    try:
        data = request.get_json() or {}
        materials = data.get("materials", [])
        client_info = data.get("client_info", {})
        project_type = data.get("project_type", "decoração")

        if not materials:
            return jsonify({"error": "Materials list is required"}), 400

        materials_text = [
            f"- {m.get('name','')} ({m.get('quantity',0)} {m.get('unit','')})"
            for m in materials
        ]
        materials_context = "\n".join(materials_text)
        client_context = f"Cliente: {client_info['name']}" if client_info.get("name") else ""

        prompt = f"""
        Você é um especialista em decoração e design de interiores. Crie uma descrição profissional e atrativa para um projeto de decoração baseado nas seguintes informações:

        {client_context}
        Tipo de projeto: {project_type}

        Materiais utilizados:
        {materials_context}

        Crie uma descrição que:
        1. Seja profissional e atrativa para o cliente
        2. Destaque os benefícios dos materiais escolhidos
        3. Mencione o resultado esperado
        4. Tenha entre 100-200 palavras
        5. Use linguagem técnica mas acessível

        Formato: Parágrafo corrido, sem bullet points.
        """

        messages = [
            {"role": "system", "content": "Você é um especialista em decoração e design de interiores."},
            {"role": "user", "content": prompt},
        ]

        try:
            description = _chat_complete(messages, max_tokens=300, temperature=0.7)
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 501

        return jsonify({"description": description.strip(), "success": True})

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar descrição: {str(e)}"}), 500


@ai_bp.route("/suggest-materials", methods=["POST"])
def suggest_materials():
    """Sugere materiais com base no tipo de projeto e requisitos."""
    try:
        data = request.get_json() or {}
        project_type = data.get("project_type", "")
        room_type = data.get("room_type", "")
        budget_range = data.get("budget_range", "")
        style = data.get("style", "")

        if not project_type:
            return jsonify({"error": "Project type is required"}), 400

        mats = Material.query.all()
        materials_list = [{
            "id": m.id,
            "name": m.nome,
            "unit": m.unidade_medida,
            "price": float(m.custo_unitario_base),
            "description": m.descricao,
        } for m in mats]

        materials_context = json.dumps(materials_list, indent=2)

        prompt = f"""
        Você é um especialista em decoração. Com base nos materiais disponíveis abaixo, sugira os 5 materiais mais adequados para o seguinte projeto:

        Tipo de projeto: {project_type}
        Tipo de ambiente: {room_type}
        Faixa de orçamento: {budget_range}
        Estilo desejado: {style}

        Materiais disponíveis:
        {materials_context}

        Para cada material sugerido, forneça:
        1. ID do material
        2. Nome do material
        3. Quantidade sugerida (número realista)
        4. Justificativa da escolha (1-2 frases)

        Responda em formato JSON com a seguinte estrutura:
        {{
          "suggestions": [
            {{
              "material_id": "id_do_material",
              "material_name": "nome_do_material",
              "suggested_quantity": numero,
              "unit": "unidade",
              "justification": "justificativa"
            }}
          ]
        }}
        """

        messages = [
            {"role": "system", "content": "Você é um especialista em decoração. Responda sempre em JSON válido."},
            {"role": "user", "content": prompt},
        ]

        try:
            ai_text = _chat_complete(messages, max_tokens=800, temperature=0.7)
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 501

        try:
            return jsonify(_json_from_ai(ai_text))
        except json.JSONDecodeError:
            return jsonify({
                "suggestions": [],
                "raw_response": ai_text,
                "note": "AI response was not in valid JSON format"
            })

    except Exception as e:
        return jsonify({"error": f"Erro ao sugerir materiais: {str(e)}"}), 500


@ai_bp.route("/analyze-pricing-trends", methods=["POST"])
def analyze_pricing_trends():
    """Analisa tendências de precificação e sugere otimizações."""
    try:
        data = request.get_json() or {}
        franchisee_id = data.get("franchisee_id")
        if not franchisee_id:
            return jsonify({"error": "Franchisee ID is required"}), 400

        projects = Project.query.filter_by(id_franqueado=franchisee_id).all()
        if not projects:
            return jsonify({
                "analysis": "Não há dados suficientes para análise de tendências. Crie mais projetos para obter insights.",
                "recommendations": []
            })

        project_data = [{
            "status": p.status,
            "total_cost": float(p.custo_total_estimado),
            "selling_price": float(p.preco_venda_sugerido),
            "margin": float(p.margem_lucro_aplicada),
            "date": p.data_criacao.isoformat()
        } for p in projects]

        projects_context = json.dumps(project_data, indent=2)

        prompt = f"""
        Você é um analista de negócios especializado em decoração. Analise os dados dos projetos abaixo e forneça insights sobre tendências de precificação:

        Dados dos projetos:
        {projects_context}

        Forneça uma análise que inclua:
        1. Tendências de preços e margens
        2. Taxa de aprovação de projetos
        3. Recomendações para otimização de preços
        4. Identificação de padrões de sucesso

        Responda em formato JSON:
        {{
          "analysis": "análise detalhada em português",
          "recommendations": ["recomendação 1", "recomendação 2", "recomendação 3"],
          "key_metrics": {{
            "average_margin": "margem média",
            "approval_rate": "taxa de aprovação",
            "average_ticket": "ticket médio"
          }}
        }}
        """

        messages = [
            {"role": "system", "content": "Você é um analista de negócios. Responda sempre em JSON válido."},
            {"role": "user", "content": prompt},
        ]

        try:
            ai_text = _chat_complete(messages, max_tokens=1000, temperature=0.7)
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 501

        try:
            return jsonify(_json_from_ai(ai_text))
        except json.JSONDecodeError:
            return jsonify({
                "analysis": ai_text,
                "recommendations": [],
                "key_metrics": {}
            })

    except Exception as e:
        return jsonify({"error": f'Erro ao analisar tendências: {str(e)}'}), 500


@ai_bp.route("/virtual-assistant", methods=["POST"])
def virtual_assistant():
    """Assistente virtual para dúvidas gerais do cliente."""
    try:
        data = request.get_json() or {}
        user_question = data.get("question", "")
        context = data.get("context", {})

        if not user_question:
            return jsonify({"error": "Question is required"}), 400

        system_context = """
        Você é um assistente virtual especializado em decoração e design de interiores. 
        Ajude com: dúvidas sobre materiais, sugestões de design, orçamento, tendências e manutenção.
        Seja profissional, prestativo, linguagem acessível. Se não souber, diga e sugira consultar um especialista.
        """

        prompt = f"""
        Pergunta do cliente: {user_question}

        Contexto adicional: {json.dumps(context, indent=2) if context else 'Nenhum contexto adicional'}

        Responda de forma clara, profissional e útil.
        """

        messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": prompt},
        ]

        try:
            answer = _chat_complete(messages, max_tokens=500, temperature=0.7)
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 501

        return jsonify({"response": answer.strip(), "success": True})

    except Exception as e:
        return jsonify({"error": f"Erro no assistente virtual: {str(e)}"}), 500


@ai_bp.route("/optimize-margins", methods=["POST"])
def optimize_margins():
    """Sugere otimizações de margem a partir de dados do projeto e mercado."""
    try:
        data = request.get_json() or {}
        project_data = data.get("project_data", {})
        market_conditions = data.get("market_conditions", {})

        if not project_data:
            return jsonify({"error": "Project data is required"}), 400

        prompt = f"""
        Você é um consultor de precificação especializado em decoração. 
        Analise os dados do projeto e sugira otimizações de margem.

        Dados do projeto:
        {json.dumps(project_data, indent=2)}

        Condições de mercado:
        {json.dumps(market_conditions, indent=2) if market_conditions else 'Não informado'}

        Responda em JSON:
        {{
          "recommended_margin": "decimal",
          "pricing_strategy": "estratégia",
          "negotiation_points": ["ponto 1", "ponto 2"],
          "risks": ["risco 1", "risco 2"],
          "opportunities": ["op 1", "op 2"]
        }}
        """

        messages = [
            {"role": "system", "content": "Você é um consultor de precificação. Responda sempre em JSON válido."},
            {"role": "user", "content": prompt},
        ]

        try:
            ai_text = _chat_complete(messages, max_tokens=800, temperature=0.7)
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 501

        try:
            return jsonify(_json_from_ai(ai_text))
        except json.JSONDecodeError:
            # fallback mínimo
            return jsonify({
                "recommended_margin": 0.30,
                "pricing_strategy": ai_text,
                "negotiation_points": [],
                "risks": [],
                "opportunities": []
            })

    except Exception as e:
        return jsonify({"error": f"Erro ao otimizar margens: {str(e)}"}), 500


@ai_bp.get("/ai/health")
def ai_health():
    """Verifica se a chave está presente (não testa conexão)."""
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    return jsonify({"openai_key": has_key})