from src.logica.Logica import Logica
from src.modelo.ingrediente import Ingrediente
from src.modelo.receta import Receta
from src.modelo.receta_ingrediente import RecetaIngrediente
from src.modelo.declarative_base import session
from faker import Faker
import unittest


class IngredienteRecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = Logica()

        self.data_factory = Faker()

        self.receta = Receta(nombre=self.data_factory.unique.text(max_nb_chars=50),
                             personas=self.data_factory.random_int(1, 50),
                             calorias=self.data_factory.random_int(1, 3000),
                             preparacion=self.data_factory.text(max_nb_chars=500),
                             tiempo=self.data_factory.time(pattern="%H:%M:%S"))
        session.add(self.receta)
        session.commit()

        self.ingrediente = Ingrediente(nombre=self.data_factory.text(max_nb_chars=50),
                                       unidad=self.data_factory.text(max_nb_chars=20),
                                       valor=self.data_factory.random_int(1, 100000),
                                       sitioCompra=self.data_factory.text(max_nb_chars=100))
        session.add(self.ingrediente)
        session.commit()


    def tearDown(self):
        busqueda0 = session.query(RecetaIngrediente).all()
        busqueda1 = session.query(Ingrediente).all()
        busqueda2 = session.query(Receta).all()

        for receta_ingrediente in busqueda0:
            session.delete(receta_ingrediente)
        
        session.commit()

        for ingrediente in busqueda1:
            session.delete(ingrediente)

        session.commit()

        for receta in busqueda2:
            session.delete(receta)

        session.commit()
        session.close()

    # Validar que si no hay ingredientes asociados a la receta, se devuelva una lista vacia.
    def test_listar_ingredientes_receta_lista_vacia(self):
        lista_ingredientes = self.logica.dar_ingredientes_receta(1)
        self.assertEqual(len(lista_ingredientes), 0)

    # Validar que si hay ingredientes asociados a la receta, se devuelva una lista con los ingredientes.
    def test_listar_ingredientes_receta_lista_llena(self):
        ingrediente_receta = RecetaIngrediente(receta_id=1,
                                               ingrediente_id=1,
                                               cantidad=self.data_factory.random_int(1, 100))
        session.add(ingrediente_receta)
        lista_ingredientes = self.logica.dar_ingredientes_receta(1)
        self.assertTrue(len(lista_ingredientes) > 0)

    # Al agregar un ingrediente a la receta con el campo "Ingrediente" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_ingrediente_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=None, ingrediente=None,
                                                             cantidad=str(self.data_factory.random_int(1, 100)))
        self.assertEqual(mensaje, "El campo ingrediente no puede ser vacío")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=self.receta, ingrediente=self.ingrediente,
                                                             cantidad="")
        self.assertEqual(mensaje, "El campo cantidad no puede ser vacío")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" como texto, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_como_texto(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=self.receta, ingrediente=self.ingrediente,
                                                             cantidad=self.data_factory.text())
        self.assertEqual(mensaje, "El campo cantidad no puede ser un texto")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" menor a cero, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_negativo(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=self.receta, ingrediente=self.ingrediente,
                                                             cantidad=str(self.data_factory.random_int(-10, -1)))
        self.assertEqual(mensaje, "El campo cantidad no puede ser negativo")

    # Al agregar un ingrediente a la receta con el campo "Cantidad" en cero, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_cantidad_cero(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=self.receta, ingrediente=self.ingrediente,
                                                             cantidad="0")
        self.assertEqual(mensaje, "El campo cantidad no puede ser cero")

    # Al agregar un ingrediente a la receta con el campo "Receta" vacio, debe lanzar un mensaje de error.
    def test_validar_crear_ingrediente_receta_campo_receta_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=None, ingrediente=self.ingrediente,
                                                             cantidad=str(self.data_factory.random_int(1, 100)))
        self.assertEqual(mensaje, "El campo receta no puede ser vacío")

    # Al agregar un ingrediente a la receta que pase todas las validaciones, se debe registrar en la base de datos.
    def test_agregar_ingrediente_receta_exitosamente(self):
        cantidad = str(self.data_factory.random_int(1, 100))
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=self.receta.to_dict(),
                                                             ingrediente=self.ingrediente.to_dict(),
                                                             cantidad=cantidad)
        ingrediente_receta_id = self.logica.agregar_ingrediente_receta(receta=self.receta.to_dict(),
                                                                       ingrediente=self.ingrediente.to_dict(),
                                                                       cantidad=cantidad)
        self.assertEqual(mensaje, "")
        self.assertTrue(ingrediente_receta_id > 0)

    # Al agregar el mismo ingrediente a la misma receta, debe lanzar un mensaje de error.
    def test_agregar_ingrediente_receta_duplicado(self):
        cantidad = str(self.data_factory.random_int(1, 100))
        ingrediente_receta_id = self.logica.agregar_ingrediente_receta(receta=self.receta.to_dict(),
                                                                       ingrediente=self.ingrediente.to_dict(),
                                                                       cantidad=cantidad)

        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                             receta=self.receta.to_dict(),
                                                             ingrediente=self.ingrediente.to_dict(),
                                                             cantidad=cantidad)
        self.assertTrue(ingrediente_receta_id > 0)
        self.assertEqual(mensaje, "El ingrediente seleccionado ya existe en la receta")

    # Al editar un ingrediente de receta campo id_ingrediente_receta vacio, debe lanzar un mensaje de error.
    def test_validar_editar_ingrediente_receta_campo_id_ingrediente_receta_vacio(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="", 
                                                             receta=self.receta.to_dict(),
                                                             ingrediente=self.ingrediente.to_dict(),
                                                             cantidad=str(self.data_factory.random_int(1, 100)))
        self.assertEqual(mensaje, "El campo id ingrediente receta no puede ser vacio")

    # Al editar un ingrediente de receta campo id_ingrediente_receta como texto, debe lanzar un mensaje de error.
    def test_validar_editar_ingrediente_receta_campo_id_ingrediente_receta_texto(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta=self.data_factory.text(), 
                                                             receta=self.receta.to_dict(),
                                                             ingrediente=self.ingrediente.to_dict(),
                                                             cantidad=str(self.data_factory.random_int(1, 100)))
        self.assertEqual(mensaje, "El campo id ingrediente receta no puede ser un texto")
    
    # Al editar un ingrediente de receta campo id_ingrediente_receta en negativo, debe lanzar un mensaje de error.
    def test_validar_editar_ingrediente_receta_campo_id_ingrediente_receta_negativo(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta=str(self.data_factory.random_int(-10, -1)), 
                                                             receta=self.receta.to_dict(),
                                                             ingrediente=self.ingrediente.to_dict(),
                                                             cantidad=str(self.data_factory.random_int(1, 100)))
        self.assertEqual(mensaje, "El campo id ingrediente receta no puede ser negativo")

    # Al editar un ingrediente de receta que no existe, debe lanzar un mensaje de error.
    def test_validar_editar_ingrediente_receta_inexistente(self):
        mensaje = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta=str(self.data_factory.random_int(1, 10)), 
                                                             receta=self.receta.to_dict(),
                                                             ingrediente=self.ingrediente.to_dict(),
                                                             cantidad=str(self.data_factory.random_int(1, 100)))
        self.assertEqual(mensaje, "El ingrediente de receta a editar no existe")

    # Al Al editar un ingrediente de receta que pase todas las validaciones, se debe actualizar en la base de datos.
    def test_editar_ingrediente_receta_exitosamente(self):
        cantidad = str(self.data_factory.random_int(1, 100))
        mensaje_1 = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta="0",
                                                               receta=self.receta.to_dict(),
                                                               ingrediente=self.ingrediente.to_dict(),
                                                               cantidad=cantidad)
        ingrediente_receta_id = self.logica.agregar_ingrediente_receta(receta=self.receta.to_dict(),
                                                                       ingrediente=self.ingrediente.to_dict(),
                                                                       cantidad=cantidad)
        mensaje_2 = self.logica.validar_crear_editar_ingReceta(id_ingrediente_receta=str(ingrediente_receta_id),
                                                               receta=self.receta.to_dict(),
                                                               ingrediente=self.ingrediente.to_dict(),
                                                               cantidad=cantidad)
        ingrediente_receta_id_2 = self.logica.editar_ingrediente_receta(id_ingrediente_receta=str(ingrediente_receta_id),
                                                                 receta=self.receta.to_dict(),
                                                                 ingrediente=self.ingrediente.to_dict(),
                                                                 cantidad=cantidad)

        self.assertEqual(mensaje_1, "")
        self.assertTrue(ingrediente_receta_id > 0)
        self.assertEqual(mensaje_2, "")
        self.assertTrue(ingrediente_receta_id_2 > 0)