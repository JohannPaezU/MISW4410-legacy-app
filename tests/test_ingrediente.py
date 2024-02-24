from src.logica.Logica import Logica
from src.modelo.ingrediente import Ingrediente
from src.modelo.declarative_base import session
import unittest


class IngredienteTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

    def tearDown(self):
        busqueda = session.query(Ingrediente).all()

        for ingrediente in busqueda:
            session.delete(ingrediente)

        session.commit()
        session.close()

    # Al crear un ingrediente con el campo "nombre" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("", "gramos", "200", "Carulla")
        self.assertEqual(mensaje, "El nombre del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "nombre" mayor a 50 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente(
            "Nombre invalido de ingrediente, cuenta con mas de 50 caracteres", "gramos", "200", "Carulla")
        self.assertEqual(mensaje, "El nombre del ingrediente no puede tener más de 50 caracteres")

    # Al crear un ingrediente con el campo "unidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "", "200", "Carulla")
        self.assertEqual(mensaje, "La unidad de medida del ingrediente no puede ser vacía")

    # Al crear un ingrediente con el campo "unidad" mayor a 20 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa",
                                                               "Unidad de medida invalida, cuenta con mas de 20 caracteres",
                                                               "200", "Carulla")
        self.assertEqual(mensaje, "La unidad de medida del ingrediente no puede tener más de 20 caracteres")

    # Al crear un ingrediente con el campo "Valor por unidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "gramos", "", "Carulla")
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "Valor por unidad" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_negativo(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "gramos", "-200", "Carulla")
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser negativo")

    # Al crear un ingrediente con el campo "Valor por unidad" igual a cero, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_cero(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "gramos", "0", "Carulla")
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser cero")

    # Al crear un ingrediente con el campo "Sitio de compra" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_sitio_compra_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "gramos", "200", "")
        self.assertEqual(mensaje, "El sitio de compra del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "Sitio de compra" mayor a 100 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_sitio_compra_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "gramos", "200",
                                                               "Sitio de compra invalido, este sitio de compra cuenta con mas de 100 caracteres, por lo tanto debe ser rechazado")
        self.assertEqual(mensaje, "El sitio de compra del ingrediente no puede tener más de 100 caracteres")

    # Al crear un ingrediente con el mismo nombre y unidad de medida de uno ya existente, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_ya_existente(self):
        self.logica.crear_ingrediente("Papa", "gramos", "200", "Carulla")
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "gramos", "200", "Carulla")
        self.assertEqual(mensaje, "Ya existe un ingrediente con el mismo nombre y unidad de medida")

    # Al crear un ingrediente que pase todas las validaciones, se debe registrar en la base de datos.
    def test_crear_ingrediente(self):
        ingrediente_id = self.logica.crear_ingrediente("Papa", "gramos", "200", "Carulla")
        self.assertTrue(ingrediente_id > 0)

    # Al crear un ingrediente con el campo "Valor por unidad" en texto, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_valor_por_unidad_texto(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "gramos", "Texto", "Carulla")
        self.assertEqual(mensaje, "El valor del ingrediente no puede ser un texto")

    # Validar que si no hay ingredientes registrados en BD, se devuelva una lista vacia.
    def test_listar_ingredientes_lista_vacia(self):
        lista_ingredientes = self.logica.dar_ingredientes()
        self.assertEqual(len(lista_ingredientes), 0)

    # Validar que si hay ingredientes registrados en BD, se devuelva una lista con los ingredientes. 
    def test_listar_ingredientes_lista_llena(self):
        consulta1 = self.logica.dar_ingredientes()
        self.logica.crear_ingrediente("Papa", "gramos", "200", "Carulla")
        consulta2 = self.logica.dar_ingredientes()
        self.assertGreater(len(consulta2), len(consulta1))
