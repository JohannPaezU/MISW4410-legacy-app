from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    unidad = Column(String)
    valor = Column(Integer)
    sitioCompra = Column(String)
    en_uso = Column(Boolean)
    recetas = relationship('Receta', secondary='receta_ingrediente')
