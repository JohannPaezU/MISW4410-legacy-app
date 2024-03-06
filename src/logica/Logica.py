from src.logica.FachadaRecetario import FachadaRecetario
from src.modelo.declarative_base import engine, Base, session
from src.modelo.ingrediente import Ingrediente
from src.modelo.receta import Receta
from src.modelo.receta_ingrediente import RecetaIngrediente
import re


class Logica(FachadaRecetario):

    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_recetas(self):
        return [elem.__dict__ for elem in session.query(Receta).order_by(Receta.nombre.asc()).all()]

    def dar_receta(self, id_receta):
        return session.query(Receta).get(id_receta).__dict__

    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        if receta == "":
            return "El nombre de la receta no puede ser vacío"
        if len(receta) > 50:
            return "El nombre de la receta no puede tener más de 50 caracteres"
        if tiempo == "":
            return "El tiempo de preparación no puede ser vacío"
        patron = r'^([0-9]{2}):([0-9]{2}):([0-9]{2})$'
        if not re.match(patron, tiempo):
            return "El tiempo de preparación no tiene el formato correcto, debe ser 'hh:mm:ss'"
        horas, minutos, segundos = map(int, tiempo.split(':'))
        if horas == 0 and minutos == 0 and segundos == 0:
            return "El tiempo de preparación no puede ser 00:00:00"
        if personas == "":
            return "El número de personas no puede ser vacío"
        try:
            int(personas)
        except ValueError:
            return "El número de personas no puede ser un texto"
        if int(personas) < 0:
            return "El número de personas no puede ser negativo"
        if int(personas) == 0:
            return "El número de personas no puede ser cero"
        if calorias == "":
            return "El número de calorías no puede ser vacío"
        try:
            int(calorias)
        except ValueError:
            return "El número de calorías no puede ser un texto"
        if int(calorias) < 0:
            return "El número de calorías no puede ser negativo"
        if int(calorias) == 0:
            return "El número de calorías no puede ser cero"
        if preparacion == "":
            return "La preparación de la receta no puede ser vacía"
        if len(preparacion) > 500:
            return "La preparación de la receta no puede tener más de 500 caracteres"
        busqueda = session.query(Receta).filter(Receta.nombre == receta).all()
        if len(busqueda) > 0:
            return "Ya existe una receta con el mismo nombre"

        return ""

    def crear_receta(self, receta, tiempo, personas, calorias, preparacion):
        receta = Receta(nombre=receta,
                        tiempo=tiempo,
                        personas=personas,
                        calorias=calorias,
                        preparacion=preparacion)
        session.add(receta)
        session.commit()

        return receta.id

    def editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        return None

    def eliminar_receta(self, id_receta):
        return None

    def dar_ingredientes(self):
        return [elem.__dict__ for elem in session.query(Ingrediente).all()]

    def dar_ingrediente(self, id_ingrediente):
        return session.query(Ingrediente).get(id_ingrediente).__dict__

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
        ingredientes =  [elem.__dict__ for elem in session.query(RecetaIngrediente)
                                                          .filter(RecetaIngrediente.receta_id == id_receta)
                                                          .all()]

        for ingrediente in ingredientes:
            ingrediente_db = self.dar_ingrediente(ingrediente["id"])
            ingrediente["ingrediente"] = ingrediente_db["nombre"]
            ingrediente["unidad"] = ingrediente_db["unidad"]

        return ingredientes

    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        receta_ingrediente = RecetaIngrediente(receta_id=receta["id"],
                                               ingrediente_id=ingrediente["id"],
                                               cantidad=cantidad)
        session.add(receta_ingrediente)
        session.commit()
        return receta_ingrediente.id

    def editar_ingrediente_receta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        ingrediente_receta = session.query(RecetaIngrediente).filter(RecetaIngrediente.id == id_ingrediente_receta).first()
        ingrediente_receta.receta_id = receta["id"]
        ingrediente_receta.ingrediente_id = ingrediente["id"]
        ingrediente_receta.cantidad = cantidad
        session.commit()
        return ingrediente_receta.id

    def validar_crear_editar_ingReceta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        if ingrediente is None:
            return "El campo ingrediente no puede ser vacío"
        if cantidad == "":
            return "El campo cantidad no puede ser vacío"
        try:
            int(cantidad)
        except ValueError:
            return "El campo cantidad no puede ser un texto"
        if int(cantidad) < 0:
            return "El campo cantidad no puede ser negativo"
        if int(cantidad) == 0:
            return "El campo cantidad no puede ser cero"
        if receta is None:
            return "El campo receta no puede ser vacío"

        busqueda = session.query(RecetaIngrediente).filter(RecetaIngrediente.receta_id == receta["id"])\
            .filter(RecetaIngrediente.ingrediente_id == ingrediente["id"]).all()
        if len(busqueda) > 0 and id_ingrediente_receta == "0":
            return "El ingrediente seleccionado ya existe en la receta"

        if id_ingrediente_receta == "":
            return "El campo id ingrediente receta no puede ser vacio"

        try:
            int(id_ingrediente_receta)
        except ValueError:
            return "El campo id ingrediente receta no puede ser un texto"

        if int(id_ingrediente_receta) < 0:
            return "El campo id ingrediente receta no puede ser negativo"

        ingrediente_receta = session.query(RecetaIngrediente).get(id_ingrediente_receta)
        if ingrediente_receta is None and id_ingrediente_receta != "0":
            return "El ingrediente de receta a editar no existe"

        return ""

    def eliminar_ingrediente_receta(self, id_ingrediente_receta, receta):
        return None

    def dar_preparacion(self, id_receta, cantidad_personas):
        return None
