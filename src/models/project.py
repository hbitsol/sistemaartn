from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
import uuid
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_franqueado = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    id_cliente = db.Column(db.String(36), db.ForeignKey('clients.id'), nullable=False)
    nome_projeto = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Rascunho')  # 'Rascunho', 'Enviado', 'Aprovado', 'Rejeitado'
    margem_lucro_aplicada = db.Column(db.Numeric(5, 2), default=0.30)  # 30% default
    custo_total_estimado = db.Column(db.Numeric(12, 2), default=0.0)
    preco_venda_sugerido = db.Column(db.Numeric(12, 2), default=0.0)
    
    # Relationships
    items = db.relationship('ProjectItem', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.nome_projeto}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_franqueado': self.id_franqueado,
            'id_cliente': self.id_cliente,
            'nome_projeto': self.nome_projeto,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'status': self.status,
            'margem_lucro_aplicada': float(self.margem_lucro_aplicada),
            'custo_total_estimado': float(self.custo_total_estimado),
            'preco_venda_sugerido': float(self.preco_venda_sugerido)
        }

class ProjectItem(db.Model):
    __tablename__ = 'project_items'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_projeto = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    id_material = db.Column(db.String(36), db.ForeignKey('materials.id'), nullable=False)
    quantidade = db.Column(db.Numeric(10, 2), nullable=False)
    id_dificuldade = db.Column(db.String(36), db.ForeignKey('difficulty_factors.id'), nullable=False)
    custo_item = db.Column(db.Numeric(10, 2), default=0.0)
    preco_venda_item = db.Column(db.Numeric(10, 2), default=0.0)
    observacoes = db.Column(db.Text)
    
    # Relationships
    material = db.relationship('Material', backref='project_items')
    difficulty = db.relationship('DifficultyFactor', backref='project_items')

    def __repr__(self):
        return f'<ProjectItem {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_projeto': self.id_projeto,
            'id_material': self.id_material,
            'quantidade': float(self.quantidade),
            'id_dificuldade': self.id_dificuldade,
            'custo_item': float(self.custo_item),
            'preco_venda_item': float(self.preco_venda_item),
            'observacoes': self.observacoes,
            'material': self.material.to_dict() if self.material else None,
            'difficulty': self.difficulty.to_dict() if self.difficulty else None
        }

