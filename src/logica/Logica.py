from src.logica.FachadaRecetario import FachadaRecetario
from src.modelo.declarative_base import engine, Base, session
from src.modelo.ingrediente import Ingrediente
from src.modelo.receta import Receta
from src.modelo.receta_ingrediente import RecetaIngrediente


class Logica(FachadaRecetario):

    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_recetas(self):
        return [elem.__dict__ for elem in session.query(Receta).order_by(Receta.nombre.asc()).all()]

    def dar_receta(self, id_receta):
        return None

    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        return None

    def crear_receta(self, receta, tiempo, personas, calorias, preparacion):
        return None

    def editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        return None

    def eliminar_receta(self, id_receta):
        return None

    def dar_ingredientes(self):
        return [elem.__dict__ for elem in session.query(Ingrediente).all()]

    def dar_ingrediente(self, id_ingrediente):
        return None

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra):
        if nombre == "":
            return "El nombre del ingrediente no puede ser vacío"

        if len(nombre) > 50:
            return "El nombre del ingrediente no puede tener más de 50 caracteres"

        if unidad == "":
            return "La unidad de medida del ingrediente no puede ser vacía"

        if len(unidad) > 20:
            return "La unidad de medida del ingrediente no puede tener más de 20 caracteres"

        if valor == "":
            return "El valor del ingrediente no puede ser vacío"

        try:
            int(valor)
        except ValueError:
            return "El valor del ingrediente no puede ser un texto"

        if int(valor) < 0:
            return "El valor del ingrediente no puede ser negativo"

        if int(valor) == 0:
            return "El valor del ingrediente no puede ser cero"

        if sitioCompra == "":
            return "El sitio de compra del ingrediente no puede ser vacío"

        if len(sitioCompra) > 100:
            return "El sitio de compra del ingrediente no puede tener más de 100 caracteres"

        busqueda = session.query(Ingrediente).filter(Ingrediente.nombre == nombre)\
            .filter(Ingrediente.unidad == unidad).all()
        if len(busqueda) > 0:
            return "Ya existe un ingrediente con el mismo nombre y unidad de medida"

        return ""

    def crear_ingrediente(self, nombre, unidad, valor, sitioCompra):
        ingrediente = Ingrediente(nombre=nombre,
                                  unidad=unidad,
                                  valor=int(valor),
                                  sitioCompra=sitioCompra,
                                  en_uso=False)
        session.add(ingrediente)
        session.commit()
        return ingrediente.id

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

    def validar_crear_editar_ingReceta(self, receta, ingrediente, cantidad):
        return None

    def eliminar_ingrediente_receta(self, id_ingrediente_receta, receta):
        return None

    def dar_preparacion(self, id_receta, cantidad_personas):
        return None
