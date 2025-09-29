# src/models/difficulty.py
from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
import uuid

class DifficultyFactor(db.Model):
    __tablename__ = "difficulty_factors"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nivel = db.Column(db.String(50), unique=True, nullable=False)  # pode ser "1", "2", "3" ou "Baixa", "Média", "Alta"
    fator_multiplicador_mao_obra = db.Column(db.Numeric(5, 2), nullable=False, default=1.0)
    descricao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<DifficultyFactor {self.nivel}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nivel": self.nivel,
            "fator_multiplicador_mao_obra": float(self.fator_multiplicador_mao_obra),
            "descricao": self.descricao,
        }