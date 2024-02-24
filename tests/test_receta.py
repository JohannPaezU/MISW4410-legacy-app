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

    # Validar que si hay recetas registradas en BD, se devuelva una lista con las recetas.
    def test_listar_recetas_lista_llena(self):
        consulta1 = self.logica.dar_recetas()
        receta = Receta(nombre="Arroz con pollo", personas=4, calorias=500, preparacion="Hervir el arroz",
                        tiempo="00:10:10")
        session.add(receta)
        session.commit()
        consulta2 = self.logica.dar_recetas()
        self.assertGreater(len(consulta2), len(consulta1))
