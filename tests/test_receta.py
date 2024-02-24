import unittest

from src.logica.Logica import Logica
from src.modelo.declarative_base import session
from src.modelo.receta import Receta


class RecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

    def tearDown(self):
        busqueda = session.query(Receta).all()

        for receta in busqueda:
            session.delete(receta)

        session.commit()
        session.close()

    # Validar que si no hay recetas registradas en BD, se devuelva una lista vacia.
    def test_listar_recetas_sin_registros(self):
        recetas = self.logica.dar_recetas()
        self.assertEqual(len(recetas), 0)
