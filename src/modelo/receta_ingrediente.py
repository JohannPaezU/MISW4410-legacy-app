from sqlalchemy import Column, Integer, ForeignKey

from .declarative_base import Base

class RecetaIngrediente(Base):
    __tablename__ = 'receta_ingrediente'

    receta_id = Column(
        Integer,
        ForeignKey('receta.id'),
        primary_key=True)

    ingrediente_id = Column(
        Integer,
        ForeignKey('ingrediente.id'),
        primary_key=True)

    cantidad_ingredientes = Column(Integer)
