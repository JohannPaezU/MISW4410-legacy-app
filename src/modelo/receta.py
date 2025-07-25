from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Receta(Base):
    __tablename__ = 'receta'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    personas = Column(Integer)
    calorias = Column(Integer)
    preparacion = Column(String)
    tiempo = Column(String)
    ingredientes = relationship('Ingrediente', secondary='receta_ingrediente')

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}