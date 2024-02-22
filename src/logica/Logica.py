from src.logica.FachadaRecetario import FachadaRecetario
from src.modelo.declarative_base import engine, Base
from src.modelo.ingrediente import Ingrediente
from src.modelo.receta import Receta
from src.modelo.receta_ingrediente import RecetaIngrediente

class Logica(FachadaRecetario):
    
    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_recetas(self):
        return None

    def dar_receta(self, id_receta):
        return None

    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        return None

    def crear_receta(self,receta, tiempo, personas, calorias, preparacion):
        return None

    def editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        return None
    
    def eliminar_receta(self, id_receta):
        return None

    def dar_ingredientes(self):
        return None

    def dar_ingrediente(self, id_ingrediente):
        return None

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra):
        return None

    def editar_ingrediente(self, id_ingrediente, nombre, unidad, valor, sitioCompras):
        return None

    def eliminar_ingrediente(self, id_ingrediente):
        return None

    def dar_ingredientes_receta(self, id_receta):
        return None

    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        return None

    def editar_ingrediente_receta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        return None

    def validar_crear_editar_ingReceta(self,receta, ingrediente, cantidad):
        return None

    def eliminar_ingrediente_receta(self, id_ingrediente_receta, receta):
        return None

    def dar_preparacion(self, id_receta,cantidad_personas):
        return None