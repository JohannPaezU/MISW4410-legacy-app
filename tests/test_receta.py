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

    # Validar que si hay recetas registradas en BD, se devuelva una lista con las recetas.
    def test_listar_recetas_alfabeticamente(self):
        receta1 = Receta(nombre="Salchipapa", personas=4, calorias=500, preparacion="Cortar papa y salchicha",
                        tiempo="00:10:10")
        receta2 = Receta(nombre="Arroz con pollo", personas=4, calorias=500, preparacion="Hervir el arroz",
                        tiempo="00:10:10")
        recetas = [receta1, receta2]
        session.add_all(recetas)
        session.commit()
        recetas_db = self.logica.dar_recetas()
        self.assertEqual(recetas_db[0]["nombre"], receta2.nombre)
        self.assertEqual(recetas_db[1]["nombre"], receta1.nombre)

    # Al crear una receta con el campo "Receta" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_receta_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta=0, receta="", tiempo="00:10:10",
                                                          personas=4, calorias=500, preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El nombre de la receta no puede ser vacío")

    # Al crear una receta con el campo "Tiempo preparación" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_tiempo_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta=0, receta="Arroz con pollo", tiempo="",
                                                          personas=4, calorias=500, preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El tiempo de preparación no puede ser vacío")

    # Al crear una receta con el campo "Tiempo preparación" sin formato "hh:mm:ss", debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_tiempo_invalido(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta=0, receta="Arroz con pollo", tiempo="10:10",
                                                          personas=4, calorias=500, preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El tiempo de preparación no tiene el formato correcto, debe ser 'hh:mm:ss'")

    # Al crear una receta con el campo "Tiempo preparación" igual a cero "00:00:00", debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_tiempo_cero(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta=0, receta="Arroz con pollo", tiempo="00:00:00",
                                                          personas=4, calorias=500, preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El tiempo de preparación no puede ser 00:00:00")

    # Al crear una receta con el campo "Número personas" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0", receta="Arroz con pollo", tiempo="00:10:10",
                                                          personas="", calorias="500", preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El número de personas no puede ser vacío")

    # Al crear una receta con el campo "Número personas" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_negativo(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0", receta="Arroz con pollo", tiempo="00:10:10",
                                                          personas="-4", calorias="500", preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El número de personas no puede ser negativo")

    # Al crear una receta con el campo "Número personas" igual a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_cero(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0", receta="Arroz con pollo", tiempo="00:10:10",
                                                          personas="0", calorias="500", preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El número de personas no puede ser cero")

    # Al crear una receta con el campo "Número personas" como texto, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_texto(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0", receta="Arroz con pollo", tiempo="00:10:10",
                                                          personas="Texto", calorias="500", preparacion="Hervir el arroz")
        self.assertEqual(mensaje, "El número de personas no puede ser un texto")