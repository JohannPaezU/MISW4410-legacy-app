from src.logica.Logica import Logica
from src.modelo.ingrediente import Ingrediente
from src.modelo.declarative_base import session
from src.modelo.receta import Receta
from faker import Faker
import unittest


class IngredienteTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

        self.data_factory = Faker()

        self.ingrediente = Ingrediente(nombre=self.data_factory.unique.text(max_nb_chars=50),
                                       unidad=self.data_factory.unique.text(max_nb_chars=20),
                                       valor=self.data_factory.random_int(1, 100000),
                                       sitioCompra=self.data_factory.text(max_nb_chars=100))
        self.receta = Receta(nombre=self.data_factory.unique.text(max_nb_chars=50),
                              personas=self.data_factory.random_int(1, 50),
                              calorias=self.data_factory.random_int(1, 3000),
                              preparacion=self.data_factory.text(max_nb_chars=500),
                              tiempo=self.data_factory.time(pattern="%H:%M:%S"))

    def tearDown(self):
        busqueda = session.query(Ingrediente).all()

        for ingrediente in busqueda:
            session.delete(ingrediente)

        session.commit()
        session.close()

    # Al crear un ingrediente con el campo "nombre" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre="",
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El nombre del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "nombre" mayor a 50 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre="X" * 51,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El nombre del ingrediente no puede tener más de 50 caracteres")

    # Al crear un ingrediente con el campo "unidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad="",
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "La unidad de medida del ingrediente no puede ser vacía")

    # Al crear un ingrediente con el campo "unidad" mayor a 20 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad="X" * 21,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "La unidad de medida del ingrediente no puede tener más de 20 caracteres")

    # Al crear un ingrediente con el campo "Valor por unidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor="",
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "Valor por unidad" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_negativo(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.data_factory.random_int(-10, -1)),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser negativo")

    # Al crear un ingrediente con el campo "Valor por unidad" igual a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_cero(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor="0",
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser cero")

    # Al crear un ingrediente con el campo "Sitio de compra" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_sitio_compra_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra="")
        self.assertEqual(mensaje, "El sitio de compra del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "Sitio de compra" mayor a 100 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_sitio_compra_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra="X" * 101)
        self.assertEqual(mensaje, "El sitio de compra del ingrediente no puede tener más de 100 caracteres")

    # Al crear un ingrediente con el mismo nombre y unidad de medida de uno ya existente, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_ya_existente(self):
        self.logica.crear_ingrediente(self.ingrediente.nombre, self.ingrediente.unidad, str(self.ingrediente.valor),
                                      self.ingrediente.sitioCompra)
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
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
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="0",
                                                               nombre=self.ingrediente.nombre,
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

    # Al editar un ingrediente con el campo "id_ingrediente" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_id_ingrediente_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente="",
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del campo id ingrediente no puede ser vacío")

    # Al editar un ingrediente con el campo "id_ingrediente" como texto, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_id_ingrediente_texto(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente=self.data_factory.text(),
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del campo id ingrediente no puede ser un texto")

    # Al editar un ingrediente con el campo "id_ingrediente" negativo, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_id_ingrediente_negativo(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente=str(self.data_factory.random_int(-10, -1)),
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El valor del campo id ingrediente no puede ser negativo")

    # Al editar un ingrediente con el campo "id_ingrediente" negativo, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_id_ingrediente_inexistente(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente=str(self.data_factory.random_int(1, 10)),
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El ingrediente a editar no existe")

    # Al editar un ingrediente que pase todas las validaciones, se debe actualizar en la base de datos.
    def test_editar_ingrediente(self):
        ingrediente_id = self.logica.crear_ingrediente(self.ingrediente.nombre, self.ingrediente.unidad,
                                                       str(self.ingrediente.valor), self.ingrediente.sitioCompra)
        mensaje = self.logica.validar_crear_editar_ingrediente(id_ingrediente=str(ingrediente_id),
                                                               nombre=self.ingrediente.nombre,
                                                               unidad=self.ingrediente.unidad,
                                                               valor=str(self.ingrediente.valor),
                                                               sitioCompra=self.ingrediente.sitioCompra)
        ingrediente_edit_id = self.logica.editar_ingrediente(id_ingrediente=str(ingrediente_id),
                                                             nombre=self.ingrediente.nombre,
                                                             unidad=self.ingrediente.unidad,
                                                             valor=str(self.ingrediente.valor),
                                                             sitioCompras=self.ingrediente.sitioCompra)
        self.assertTrue(ingrediente_id > 0)
        self.assertEqual(mensaje, "")
        self.assertTrue(ingrediente_edit_id > 0)

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

    # Al eliminar un ingrediente con el campo "id_ingrediente" inexistente, debe lanzar un mensaje de error.
    def test_eliminar_ingrediente_id_inexistente(self):
        with self.assertRaises(ValueError) as contexto:
            self.logica.eliminar_ingrediente(str(self.data_factory.random_int(-100, -2)))
        self.assertEqual(str(contexto.exception), "No existe un ingrediente con el id especificado")

    # Al eliminar un ingrediente con el campo "id_ingrediente" existente, se debe eliminar de la base de datos.
    def test_eliminar_ingrediente(self):
        consulta1 = self.logica.dar_ingredientes()
        ingrediente_id = self.logica.crear_ingrediente(self.ingrediente.nombre, self.ingrediente.unidad,
                                                       str(self.ingrediente.valor), self.ingrediente.sitioCompra)
        self.logica.eliminar_ingrediente(str(ingrediente_id))
        consulta2 = self.logica.dar_ingredientes()
        self.assertEqual(len(consulta2), len(consulta1))

    # Al eliminar un ingrediente que esté asociado a una receta, debe lanzar un mensaje de error.
    def test_eliminar_ingrediente_asociado_a_receta(self):
        receta_id = self.logica.crear_receta(receta=self.receta.nombre,
                                             tiempo=self.receta.tiempo,
                                             personas=str(self.receta.personas),
                                             calorias=str(self.receta.calorias),
                                             preparacion=self.receta.preparacion)
        ingrediente_id = self.logica.crear_ingrediente(self.ingrediente.nombre, self.ingrediente.unidad,
                                                       str(self.ingrediente.valor), self.ingrediente.sitioCompra)

        self.logica.agregar_ingrediente_receta(receta=self.logica.dar_receta(receta_id),
                                               ingrediente=self.logica.dar_ingrediente(ingrediente_id),
                                               cantidad=self.data_factory.random_int(1, 100))
        with self.assertRaises(ValueError) as contexto:
            self.logica.eliminar_ingrediente(ingrediente_id)
        self.assertEqual(str(contexto.exception), "No se puede eliminar un ingrediente que esté asociado a una receta")
