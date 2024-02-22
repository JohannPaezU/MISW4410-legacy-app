from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Receta(Base):
    __tablename__ = 'receta'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    numero_personas = Column(Integer)
    calorias_porcion = Column(Integer)
    instrucciones = Column(String)
    tiempo_preparacion = Column(String)
    ingredientes = relationship('Ingrediente', secondary='receta_ingrediente')
