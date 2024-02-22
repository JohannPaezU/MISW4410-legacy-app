from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    unidad_medida = Column(String)
    valor_unidad = Column(Integer)
    lugar_compra = Column(String)
    en_uso = Column(Boolean)
    recetas = relationship('Receta', secondary='receta_ingrediente')
