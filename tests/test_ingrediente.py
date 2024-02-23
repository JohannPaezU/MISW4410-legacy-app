from src.logica.Logica import Logica
import unittest

class IngredienteTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()
        
    def tearDown(self):
        self.logica = None
    
    # Al crear un ingrediente con el campo "nombre" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("", "gramos", "200", "Carulla")
        self.assertEqual(mensaje, "El nombre del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "nombre" mayor a 50 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_nombre_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Nombre invalido de ingrediente, cuenta con mas de 50 caracteres", "gramos", "200", "Carulla")
        self.assertEqual(mensaje, "El nombre del ingrediente no puede tener más de 50 caracteres")

    # Al crear un ingrediente con el campo "unidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "", "200", "Carulla")
        self.assertEqual(mensaje, "La unidad de medida del ingrediente no puede ser vacía")

    # Al crear un ingrediente con el campo "unidad" mayor a 20 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_campo_unidad_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Papa", "Unidad de medida invalida, cuenta con mas de 20 caracteres", "200", "Carulla")
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