from src.logica.Logica import Logica
from src.modelo.ingrediente import Ingrediente
from src.modelo.declarative_base import session
from faker import Faker
import unittest


class IngredienteTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

        self.data_factory = Faker()

        self.ingrediente = Ingrediente(nombre=self.data_factory.unique.text(max_nb_chars=50),
                                       unidad=self.data_factory.unique.text(max_nb_chars=20),
                                       valor=self.data_factory.random_int(1, 100000),
                                       sitioCompra=self.data_factory.text(max_nb_chars=100),
                                       en_uso=self.data_factory.boolean())

    def tearDown(self):
        busqueda = session.query(Ingrediente).all()

        for ingrediente in busqueda:
            session.delete(ingrediente)

        session.commit()
        session.close()

    # Al crear un ingrediente con el campo "nombre" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre="",
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El nombre del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "nombre" mayor a 50 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre="X" * 51,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El nombre del ingrediente no puede tener más de 50 caracteres")

    # Al crear un ingrediente con el campo "unidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad="",
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "La unidad de medida del ingrediente no puede ser vacía")

    # Al crear un ingrediente con el campo "unidad" mayor a 20 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad="X" * 21,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "La unidad de medida del ingrediente no puede tener más de 20 caracteres")

    # Al crear un ingrediente con el campo "Valor por unidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor="",
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "Valor por unidad" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_negativo(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.data_factory.random_int(-10, -1)),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser negativo")

    # Al crear un ingrediente con el campo "Valor por unidad" igual a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_cero(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor="0",
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser cero")

    # Al crear un ingrediente con el campo "Sitio de compra" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_sitio_compra_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra="")
        self.assertEqual(mensaje, "El sitio de compra del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "Sitio de compra" mayor a 100 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_sitio_compra_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra="X" * 101)
        self.assertEqual(mensaje, "El sitio de compra del ingrediente no puede tener más de 100 caracteres")

    # Al crear un ingrediente con el mismo nombre y unidad de medida de uno ya existente, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_ya_existente(self):
        self.logica.crear_ingrediente(self.ingrediente.nombre, self.ingrediente.unidad, str(self.ingrediente.valor),
                                      self.ingrediente.sitioCompra)
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "Ya existe un ingrediente con el mismo nombre y unidad de medida")

    # Al crear un ingrediente que pase todas las validaciones, se debe registrar en la base de datos.
    def test_crear_ingrediente(self):
        ingrediente_id = self.logica.crear_ingrediente(self.ingrediente.nombre, self.ingrediente.unidad,
                                                       str(self.ingrediente.valor), self.ingrediente.sitioCompra)
        self.assertTrue(ingrediente_id > 0)

    # Al crear un ingrediente con el campo "Valor por unidad" en texto, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_texto(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=self.data_factory.text(),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser un texto")

    # Validar que si no hay ingredientes registrados en BD, se devuelva una lista vacia.
    def test_listar_ingredientes_lista_vacia(self):
        lista_ingredientes = self.logica.dar_ingredientes()
        self.assertEqual(len(lista_ingredientes), 0)

    # Validar que si hay ingredientes registrados en BD, se devuelva una lista con los ingredientes. 
    def test_listar_ingredientes_lista_llena(self):
        consulta1 = self.logica.dar_ingredientes()
        self.logica.crear_ingrediente(self.ingrediente.nombre, self.ingrediente.unidad, str(self.ingrediente.valor),
                                      self.ingrediente.sitioCompra)
        consulta2 = self.logica.dar_ingredientes()
        self.assertGreater(len(consulta2), len(consulta1))

    # Al eliminar un ingrediente con el campo "id_ingrediente" vacio, debe lanzar un mensaje de error.
    def test_eliminar_ingrediente_campo_id_ingrediente_vacio(self):
        with self.assertRaises(ValueError) as contexto:
            self.logica.eliminar_ingrediente("")
        self.assertEqual(str(contexto.exception), "El campo id de ingrediente no puede ser vacío")

    # Al eliminar un ingrediente con el campo "id_ingrediente" como texto, debe lanzar un mensaje de error
    def test_eliminar_ingrediente_campo_id_ingrediente_texto(self):
        with self.assertRaises(ValueError) as contexto:
            self.logica.eliminar_ingrediente(self.data_factory.text())
        self.assertEqual(str(contexto.exception), "El campo id de ingrediente debe ser un número")
