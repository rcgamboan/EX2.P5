import unittest
import manejador

# para ejecutar las pruebas y calcular la cobertura ejecutar el siguiente comando:
# coverage run -m unittest tests.py
# Luego se puede acceder al reporte de la cobertura con el comando
# coverage report
class Tests(unittest.TestCase):

    def test_agregar_Atomo(self):
        self.assertTrue(manejador.agregarTipo("p1",1,4))
    
    def test_agregar_Atomo_existente(self):
        manejador.agregarTipo("p2",1,2)
        self.assertFalse(manejador.agregarTipo("p2",4,7))
    
    def test_agregar_Union(self):
        manejador.agregarTipo("int",4,4)
        manejador.agregarTipo("char",1,4)
        self.assertTrue(manejador.agregarUnion("u1",["int","char"]))
    
    def test_agregar_Union_existente(self):
        manejador.agregarTipo("bool",4,4)
        manejador.agregarTipo("string",2,4)
        manejador.agregarUnion("u2",["bool","string"])
        self.assertFalse(manejador.agregarUnion("u2",["bool","string"]))
    
    def test_agregar_Struct(self):
        manejador.agregarTipo("byte",1,1)
        manejador.agregarTipo("short",2,2)
        self.assertTrue(manejador.agregarUnion("s1",["byte","short"]))
    
    def test_agregar_Struct_existente(self):
        manejador.agregarTipo("long",8,8)
        manejador.agregarTipo("long long",16,16)
        manejador.agregarUnion("s2",["long","long long"])
        self.assertFalse(manejador.agregarUnion("s2",["long","long"]))
    
    def test_describir_atomo(self):
        manejador.agregarTipo("long",8,8)
        self.assertTrue(manejador.describir("long"))
    
    def test_describir_struct(self):
        manejador.agregarTipo("long",8,8)
        manejador.agregarTipo("short",2,2)
        manejador.agregarStruct("d1",["long","short"])
        self.assertTrue(manejador.describir("d1"))
    
    def test_describir_union(self):
        manejador.agregarTipo("long",8,8)
        manejador.agregarTipo("short",2,2)
        manejador.agregarUnion("d2",["long","short"])
        self.assertTrue(manejador.describir("d2"))
    
    

if __name__ == '__main__':
    unittest.main()