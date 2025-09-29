from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
import uuid

class Franchise(db.Model):
    __tablename__ = 'franchises'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome_franquia = db.Column(db.String(200), unique=True, nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    endereco = db.Column(db.String(500))
    telefone = db.Column(db.String(20))
    
    # Relationship with users
    users = db.relationship('User', backref='franchise', lazy=True)

    def __repr__(self):
        return f'<Franchise {self.nome_franquia}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_franquia': self.nome_franquia,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'telefone': self.telefone
        }

