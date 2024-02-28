from src.logica.Logica import Logica
from src.modelo.ingrediente import Ingrediente
from src.modelo.receta import Receta
from src.modelo.receta_ingrediente import RecetaIngrediente
from src.modelo.declarative_base import session
import unittest


class IngredienteRecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

    def tearDown(self):
        busqueda0 = session.query(RecetaIngrediente).all()
        busqueda1 = session.query(Ingrediente).all()
        busqueda2 = session.query(Receta).all()

        for receta_ingrediente in busqueda0:
            session.delete(receta_ingrediente)

        for ingrediente in busqueda1:
            session.delete(ingrediente)

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
        receta = Receta(nombre="Arroz con pollo",
                        personas=4, calorias=500,
                        preparacion="Hervir el arroz",
                        tiempo="00:10:10")
        session.add(receta)
        ingrediente_id = self.logica.crear_ingrediente("Papa", "gramos", "200", "Carulla")
        ingrediente_receta = RecetaIngrediente(receta_id=1,
                                               ingrediente_id=ingrediente_id,
                                               cantidad_ingredientes=5)
        session.add(ingrediente_receta)
        lista_ingredientes = self.logica.dar_ingredientes_receta(1)
        self.assertTrue(len(lista_ingredientes) > 0)