from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
import uuid
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_franqueado = db.Column(db.String(36), db.ForeignKey('franchises.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(500))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Client {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_franqueado': self.id_franqueado,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }

