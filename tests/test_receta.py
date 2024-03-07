import unittest

from src.logica.Logica import Logica
from src.modelo.declarative_base import session
from src.modelo.receta import Receta
from faker import Faker


class RecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()
        self.data_factory = Faker()

        self.receta1 = Receta(nombre=self.data_factory.unique.text(max_nb_chars=50),
                                   personas=self.data_factory.random_int(1, 50),
                                   calorias=self.data_factory.random_int(1, 3000),
                                   preparacion=self.data_factory.text(max_nb_chars=500),
                                   tiempo=self.data_factory.time(pattern="%H:%M:%S"))

        self.receta2 = Receta(nombre=self.data_factory.unique.text(max_nb_chars=50),
                                    personas=self.data_factory.random_int(1, 50),
                                    calorias=self.data_factory.random_int(1, 3000),
                                    preparacion=self.data_factory.text(max_nb_chars=500),
                                    tiempo=self.data_factory.time(pattern="%H:%M:%S"))

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
        session.add(self.receta1)
        session.commit()
        consulta2 = self.logica.dar_recetas()
        self.assertGreater(len(consulta2), len(consulta1))

    # Validar que si hay recetas registradas en BD, se devuelva una lista con las recetas.
    def test_listar_recetas_alfabeticamente(self):
        recetas = [self.receta2, self.receta1]
        session.add_all(recetas)
        session.commit()
        recetas_db = self.logica.dar_recetas()
        recetas.sort(key=lambda receta: receta.nombre)
        self.assertEqual(recetas_db[0]["nombre"], recetas[0].nombre)
        self.assertEqual(recetas_db[1]["nombre"], recetas[1].nombre)

    # Al crear una receta con el campo "Receta" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_receta_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta="",
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El nombre de la receta no puede ser vacío")

    # Al crear una receta con el campo "Receta" mayor a 50 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_receta_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta="X" * 51,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El nombre de la receta no puede tener más de 50 caracteres")


    # Al crear una receta con el campo "Tiempo preparación" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_tiempo_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo="",
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El tiempo de preparación no puede ser vacío")

    # Al crear una receta con el campo "Tiempo preparación" sin formato "hh:mm:ss", debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_tiempo_invalido(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.data_factory.time(pattern="%H:%M"),
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El tiempo de preparación no tiene el formato correcto, debe ser 'hh:mm:ss'")

    # Al crear una receta con el campo "Tiempo preparación" igual a cero "00:00:00", debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_tiempo_cero(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo="00:00:00",
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El tiempo de preparación no puede ser 00:00:00")

    # Al crear una receta con el campo "Número personas" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas="",
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de personas no puede ser vacío")

    # Al crear una receta con el campo "Número personas" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_negativo(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.data_factory.random_int(-10, -1)),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de personas no puede ser negativo")

    # Al crear una receta con el campo "Número personas" igual a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_cero(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas="0",
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de personas no puede ser cero")

    # Al crear una receta con el campo "Número personas" como texto, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_personas_texto(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=self.data_factory.text(),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de personas no puede ser un texto")

    # Al crear una receta con el campo "Calorias por porción" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_calorias_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias="",
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de calorías no puede ser vacío")

    # Al crear una receta con el campo "Calorias por porción" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_calorias_negativo(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.data_factory.random_int(-10, -1)),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de calorías no puede ser negativo")

    # Al crear una receta con el campo "Calorias por porción" igual a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_calorias_cero(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias="0",
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de calorías no puede ser cero")

    # Al crear una receta con el campo "Calorias por porción" como texto, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_calorias_texto(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0", 
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=self.data_factory.text(),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El número de calorías no puede ser un texto")

    # Al crear una receta con el campo "Preparación" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_preparacion_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion="")
        self.assertEqual(mensaje, "La preparación de la receta no puede ser vacía")

    # Al crear una receta con el campo "Preparación" mayor a 500 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_preparacion_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion="X" * 501)
        self.assertEqual(mensaje, "La preparación de la receta no puede tener más de 500 caracteres")

    # Al crear una receta con el mismo nombre de una ya existente, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_ya_existente(self):
        session.add(self.receta1)
        session.commit()
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "Ya existe una receta con el mismo nombre")

    # Al crear una receta que pase todas las validaciones, se debe registrar en la base de datos.
    def test_crear_receta(self):
        receta = self.receta1.nombre
        tiempo = self.receta1.tiempo
        personas = str(self.receta1.personas)
        calorias = str(self.receta1.calorias)
        preparacion = self.receta1.preparacion
        mensaje = self.logica.validar_crear_editar_receta(id_receta="0",
                                                          receta=receta,
                                                          tiempo=tiempo,
                                                          personas=personas,
                                                          calorias=calorias,
                                                          preparacion=preparacion)
        receta_id = self.logica.crear_receta(receta=receta,
                                             tiempo=tiempo,
                                             personas=personas,
                                             calorias=calorias,
                                             preparacion=preparacion)
        self.assertEqual(mensaje, "")
        self.assertTrue(receta_id > 0)

    # Al editar una receta con el campo "id_receta" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_id_receta_vacio(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta="",
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El id de la receta no puede ser vacío")

    # Al editar una receta con el campo "id_receta" como texto, debe lanzar un mensaje de error.
    def test_validar_crear_editar_receta_campo_id_receta_texto(self):
        mensaje = self.logica.validar_crear_editar_receta(id_receta=self.data_factory.text(),
                                                          receta=self.receta1.nombre,
                                                          tiempo=self.receta1.tiempo,
                                                          personas=str(self.receta1.personas),
                                                          calorias=str(self.receta1.calorias),
                                                          preparacion=self.receta1.preparacion)
        self.assertEqual(mensaje, "El id de la receta no puede ser un texto")
