from src.logica.Logica import Logica
from src.modelo.ingrediente import Ingrediente
from src.modelo.receta import Receta
from src.modelo.receta_ingrediente import RecetaIngrediente
from src.modelo.declarative_base import session
import unittest


class IngredienteRecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

        self.receta = Receta(nombre="Arroz con pollo",
                        personas=4, calorias=500,
                        preparacion="Hervir el arroz",
                        tiempo="00:10:10")
        session.add(self.receta)

        self.ingrediente = Ingrediente(nombre="Papa",
                            unidad="gramos",
                            valor= 200,
                            sitioCompra="Carulla",
                            en_uso=False)
        session.add(self.ingrediente)


    def tearDown(self):
        busqueda0 = session.query(RecetaIngrediente).all()
        busqueda1 = session.query(Ingrediente).all()
        busqueda2 = session.query(Receta).all()

        for receta_ingrediente in busqueda0:
            session.delete(receta_ingrediente)
        
        session.commit()

        for ingrediente in busqueda1:
            session.delete(ingrediente)

        session.commit()

        for receta in busqueda2:
            session.delete(receta)

        session.commit()
        session.close()

    # Validar que si no hay ingredientes asociados a la receta, se devuelva una lista vacia.
    def test_listar_ingredientes_receta_lista_vacia(self):
        lista_ingredientes = self.logica.dar_ingredientes_receta(1)
        self.assertEqual(len(lista_ingredientes), 0)

    # Validar que si hay ingredientes asociados a la receta, se devuelva una lista con los ingredientes.
    def test_listar_ingredientes_receta_lista_llena(self):
        ingrediente_receta = RecetaIngrediente(receta_id=1,
                                               ingrediente_id=1,
                                               cantidad_ingredientes=5)
        session.add(ingrediente_receta)
        lista_ingredientes = self.logica.dar_ingredientes_receta(1)
        self.assertTrue(len(lista_ingredientes) > 0)

    # Al agregar un ingrediente a la receta con el campo "Ingrediente" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_ingrediente_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(receta=None, ingrediente=None, cantidad="5")
        self.assertEqual(mensaje, "El campo ingrediente no puede ser vacío")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(receta=self.receta, ingrediente=self.ingrediente, cantidad="")
        self.assertEqual(mensaje, "El campo cantidad no puede ser vacío")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" como texto, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_como_texto(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(receta=self.receta, ingrediente=self.ingrediente, cantidad="hola")
        self.assertEqual(mensaje, "El campo cantidad no puede ser un texto")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_negativo(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(receta=self.receta, ingrediente=self.ingrediente, cantidad="-5")
        self.assertEqual(mensaje, "El campo cantidad no puede ser negativo")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" en cero, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_cero(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(receta=self.receta, ingrediente=self.ingrediente, cantidad="0")
        self.assertEqual(mensaje, "El campo cantidad no puede ser cero")