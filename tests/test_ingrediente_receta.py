from src.logica.Logica import Logica
from src.modelo.ingrediente import Ingrediente
from src.modelo.declarative_base import session
import unittest


class IngredienteRecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

    def tearDown(self):
        busqueda = session.query(Ingrediente).all()

        for ingrediente in busqueda:
            session.delete(ingrediente)

        session.commit()
        session.close()

    # Validar que si no hay ingredientes asociados a la receta, se devuelva una lista vacia.
    def test_listar_ingredientes_receta_lista_vacia(self):
        lista_ingredientes = self.logica.dar_ingredientes_receta(1)
        self.assertEqual(len(lista_ingredientes), 0)