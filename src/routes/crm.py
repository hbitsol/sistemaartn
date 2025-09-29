from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.client import Client
from src.models.project import Project, ProjectItem
from src.models.material import Material
from src.models.difficulty import DifficultyFactor
from decimal import Decimal

crm_bp = Blueprint('crm', __name__)

# Client Management Routes
@crm_bp.route('/clients', methods=['GET'])
def get_clients():
    """Get all clients for a franchisee"""
    try:
        # In a real app, you'd get the franchisee ID from authentication
        # For now, we'll use a query parameter or get all clients
        franchisee_id = request.args.get('franchisee_id')
        
        if franchisee_id:
            clients = Client.query.filter_by(id_franqueado=franchisee_id).all()
        else:
            clients = Client.query.all()
        
        return jsonify([client.to_dict() for client in clients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/clients', methods=['POST'])
def create_client():
    """Create a new client"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['nome', 'id_franqueado']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        client = Client(
            nome=data['nome'],
            email=data.get('email', ''),
            telefone=data.get('telefone', ''),
            endereco=data.get('endereco', ''),
            id_franqueado=data['id_franqueado']
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'client': client.to_dict(),
            'message': 'Client created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    """Get a specific client"""
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        return jsonify(client.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/clients/<client_id>', methods=['PUT'])
def update_client(client_id):
    """Update a client"""
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'nome' in data:
            client.nome = data['nome']
        if 'email' in data:
            client.email = data['email']
        if 'telefone' in data:
            client.telefone = data['telefone']
        if 'endereco' in data:
            client.endereco = data['endereco']
        
        db.session.commit()
        
        return jsonify({
            'client': client.to_dict(),
            'message': 'Client updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/clients/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Delete a client"""
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        # Check if client has projects
        projects = Project.query.filter_by(id_cliente=client_id).count()
        if projects > 0:
            return jsonify({'error': 'Cannot delete client with existing projects'}), 400
        
        db.session.delete(client)
        db.session.commit()
        
        return jsonify({'message': 'Client deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Project Management Routes
@crm_bp.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects for a franchisee"""
    try:
        franchisee_id = request.args.get('franchisee_id')
        client_id = request.args.get('client_id')
        
        query = Project.query
        
        if franchisee_id:
            query = query.filter_by(id_franqueado=franchisee_id)
        if client_id:
            query = query.filter_by(id_cliente=client_id)
        
        projects = query.all()
        
        # Include client information in the response
        result = []
        for project in projects:
            project_data = project.to_dict()
            client = Client.query.get(project.id_cliente)
            if client:
                project_data['client'] = client.to_dict()
            result.append(project_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/projects/<project_id>/items', methods=['GET'])
def get_project_items(project_id):
    """Get all items for a specific project"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        items = ProjectItem.query.filter_by(id_projeto=project_id).all()
        return jsonify([item.to_dict() for item in items])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/projects/<project_id>/status', methods=['PUT'])
def update_project_status(project_id):
    """Update project status"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.get_json()
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        valid_statuses = ['Rascunho', 'Enviado', 'Aprovado', 'Rejeitado']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
        
        project.status = data['status']
        db.session.commit()
        
        return jsonify({
            'project': project.to_dict(),
            'message': 'Project status updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project and all its items"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Delete all project items first (cascade should handle this, but being explicit)
        ProjectItem.query.filter_by(id_projeto=project_id).delete()
        
        # Delete the project
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@crm_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics for a franchisee"""
    try:
        franchisee_id = request.args.get('franchisee_id')
        
        if not franchisee_id:
            return jsonify({'error': 'franchisee_id is required'}), 400
        
        # Get statistics
        total_clients = Client.query.filter_by(id_franqueado=franchisee_id).count()
        total_projects = Project.query.filter_by(id_franqueado=franchisee_id).count()
        
        # Projects by status
        projects_by_status = {}
        statuses = ['Rascunho', 'Enviado', 'Aprovado', 'Rejeitado']
        for status in statuses:
            count = Project.query.filter_by(id_franqueado=franchisee_id, status=status).count()
            projects_by_status[status] = count
        
        # Total revenue from approved projects
        approved_projects = Project.query.filter_by(
            id_franqueado=franchisee_id, 
            status='Aprovado'
        ).all()
        
        total_revenue = sum(float(project.preco_venda_sugerido) for project in approved_projects)
        
        return jsonify({
            'total_clients': total_clients,
            'total_projects': total_projects,
            'projects_by_status': projects_by_status,
            'total_revenue': total_revenue,
            'approved_projects_count': len(approved_projects)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

