from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
import uuid
from datetime import datetime

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(200), unique=True, nullable=False)
    unidade_medida = db.Column(db.String(10), nullable=False, default='unidade')  # 'm', 'm²', 'un', 'L', 'kg'
    custo_unitario_base = db.Column(db.Numeric(10, 2), nullable=False,  default=0)
    descricao = db.Column(db.Text)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Material {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'unidade_medida': self.unidade_medida,
            'custo_unitario_base': float(self.custo_unitario_base),
            'descricao': self.descricao,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

