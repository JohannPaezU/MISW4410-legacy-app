from src.logica.Logica import Logica
import unittest

class IngredienteTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()
        
    def tearDown(self):
        self.logica = None
    
    # Al crear un ingrediente con el campo "nombre" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_nombre_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("", "gramos", "200", "Carulla")
        self.assertEqual(mensaje, "El nombre del ingrediente no puede ser vacío")

    # Al crear un ingrediente con el campo "nombre" mayor a 50 caracteres, debe lanzar un mensaje de error.
    def test_validar_crear_editar_ingrediente_nombre_con_longitud_invalida(self):
        mensaje = self.logica.validar_crear_editar_ingrediente("Nombre invalido de ingrediente, cuenta con mas de 50 caracteres", "gramos", "200", "Carulla")
        self.assertEqual(mensaje, "El nombre del ingrediente no puede tener más de 50 caracteres")

