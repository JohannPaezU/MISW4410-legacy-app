from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from .declarative_base import Base


class RecetaIngrediente(Base):
    __tablename__ = 'receta_ingrediente'

    id = Column(Integer, primary_key=True)
    receta_id = Column(
        Integer,
        ForeignKey('receta.id'))

    ingrediente_id = Column(
        Integer,
        ForeignKey('ingrediente.id'))

    cantidad_ingredientes = Column(Integer)
    __table_args__ = (
        UniqueConstraint('receta_id', 'ingrediente_id'),
    )
