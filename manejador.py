import itertools

# implementacion del manejador de tipos de datos
dicStruct = {}
dicUnion = {}
dicTipos = {}

# Se crean las clases Atomo, Struct y Union para simular los tipos de datos requeridos

class Atomo:
    def __init__(self,representacion,alineacion):
        self.representacion = representacion
        self.alineacion = alineacion

class Struct:
    
    def __init__(self,nombre : str,tipos : str):
        self.nombre = nombre
        self.tipos = tipos

class Union:

    def __init__(self,nombre:str,tipos:str):
        self.nombre = nombre
        self.tipos = tipos

# Metodo para agregar un nuevo tipo atomo
# se verifica si el nombre ya se encuentra asociado a algun otro tipo
# caso contrario se agrega el tipo al diccionario correspondiente
def agregarTipo(nombre,representacion,alineacion):
    if dicTipos.get(nombre) != None or dicStruct.get(nombre) != None or dicUnion.get(nombre) != None:
        print("El tipo " + nombre + " ya se encuentra definido")
        return False
    dicTipos[nombre] = Atomo(representacion,alineacion)
    return True

# Metodo para agregar un nuevo tipo struct
# se verifica si el nombre ya se encuentra asociado a algun otro tipo
# caso contrario se agrega el tipo al diccionario correspondiente
def agregarStruct(nombre, tipos):
    
    if dicTipos.get(nombre) != None or dicStruct.get(nombre) != None or dicUnion.get(nombre) != None:
        print(nombre + " ya se encuentra definido")
        return
    listaTipos = []
    print(tipos)
    for tipo in tipos:
        if dicTipos.get(tipo) == None:
            print("el tipo " + tipo + " no se encuentra definido")
            return False
        listaTipos.append(tipo)
    dicStruct[nombre] = Struct(nombre,listaTipos)
    return True

# Metodo para agregar un nuevo tipo union
# se verifica si el nombre ya se encuentra asociado a algun otro tipo
# caso contrario se agrega el tipo al diccionario correspondiente
def agregarUnion(nombre, tipos):
    
    if dicTipos.get(nombre) != None or dicStruct.get(nombre) != None or dicUnion.get(nombre) != None:
        print(nombre + " ya se encuentra definido")
        return False
    for tipo in tipos:
        if dicTipos.get(tipo) == None:
            print("el tipo " + tipo + " no se encuentra definido")
            return False
    dicUnion[nombre] = Union(nombre,tipos)
    return True

# metodo para describir el tipo con nombre solicitado
def describir(nombre):

    # se verifica si existe un tipo asociado al nombre
    if dicUnion.get(nombre) == None and dicStruct.get(nombre) == None and dicTipos.get(nombre) == None:
        print(nombre + " no se encuentra definido")
        return
    else:
        # se obtiene el tipo correspondiente al nombre
        objeto = obtenerTipo(nombre)

        if isinstance(objeto,Atomo):
            print(f"\nTipo Atomo {nombre}")
        elif isinstance(objeto,Struct):
            print(f"\nTipo Struct {nombre}")
        elif isinstance(objeto,Union):
            print(f"\nTipo Union {nombre}")

        size = obtenerEspacio(objeto)
        alineacion = obtenerAlineacion(objeto)
        # Si se empaquetan registros y registros invariantes no hay desperdicio
        # El tamanio y la alineacion son las dadas por el mismo tipo
        print("\nSi el lenguaje guarda registros y registros variantes empaquetados:")
        print(f"Ocupacion : {size}\nAlineacion : {alineacion}\nDesperdicio : 0")

        
        size, desperdicio = obtenerEspacioyDesperdiciosinEmpaquetar(objeto)
        # Si no se empaquetan los registros ni registros invariantes, se calcula el desperdicio
        # La alineacion sigue siendo la misma
        print("\nSi el lenguaje guarda registros y registros variantes sin empaquetar:")
        print(f"Ocupacion : {size+desperdicio}\nAlineacion : {alineacion}\nDesperdicio : {desperdicio}")

        # si se reordenan los registros, se calculan las formas posibles de reordenar y se selecciona la mas optima
        # La alineacion sigue siendo la misma
        (size, desperdicio) = reordenar(objeto)
        print("\nSi el lenguaje guarda registros y registros variantes reordenando los campos de manera óptima:")
        print(f"Ocupacion : {size}\nAlineacion : {alineacion}\nDesperdicio : {desperdicio}")
    return True

# metodo que devuelve el espacio y desperdicio del tipo suministrado
# si se llama con un tipo atomo, se devuelve su atributo representacion
# y como desperdicio se devuelve la resta entre su alineacion y su representacion
# si se llama con un tipo union, se encuentra su tipo atomo con mayor representacion y se realiza el mismo proceso que un tipo atomo
# si se llama con un tipo struct, se obtiene la informacion por cada tipo atomo almacenado y se suma
def obtenerEspacioyDesperdiciosinEmpaquetar(tipo):

    if isinstance(tipo, Atomo):
        # El desperdicio de un atomo viene dado por la diferencia entre su alineacion y su representacion
        desperdicio = obtenerAlineacion(tipo) - tipo.representacion
        return tipo.representacion, desperdicio

    elif isinstance(tipo, Union):
        
        tipos = tipo.tipos
        listaTipos = []
        for elem in tipos:
            listaTipos.append(dicTipos[elem])
        atom = max(listaTipos, key=lambda Atomo: Atomo.representacion)
        desperdicio = obtenerAlineacion(atom) - atom.representacion

        return atom.representacion, desperdicio

    else:
        # por cada tipo atomo del struct, se calcula su espacio y desperdicio
        # y el espacio ocupado y desperdicio es la suma del espacio y desperdicio de cada uno de sus tipos atomo
        size = 0
        sizeAct = 0
        desperdicio = 0
        desperdicioAct = 0
        for tipo in tipo.tipos:
            atom = dicTipos[tipo]
            desperdicioAct = obtenerAlineacion(atom) - atom.representacion
            sizeAct = atom.representacion
            size+= sizeAct
            desperdicio += desperdicioAct

        return size, desperdicio

def reordenar(tipo):

    if isinstance(tipo, Atomo):
        # si se trata de un tipo atomo, no hay nada que reordenar
        # se devuelve su desperdicio y su espacio ocupado
        desperdicio = obtenerAlineacion(tipo) - tipo.representacion
        return (tipo.representacion, desperdicio)

    elif isinstance(tipo, Union):
        # si se trata de un tipo union, tampoco hay nada que reordenar
        # ya que en memoria en todo momento se almacena un solo tipo atomo a la vez
        # se devuelve el desperdicio y espacio ocupado del tipo atomo con mayor representacion
        tipos = tipo.tipos
        listaTipos = []
        for elem in tipos:
            listaTipos.append(dicTipos[elem])
        atom = max(listaTipos, key=lambda Atomo: Atomo.representacion)
        desperdicio = obtenerAlineacion(atom) - atom.representacion

        return atom.representacion, desperdicio

    else:
        # si se trata de un tipo struct, se obtienen todos los posibles ordenamientos de los tipos atomos
        # se calcula la ocupacion y desperdicio de cada tipo
        # y se devuelve la mas optima
        
        # Se consigue todas las permutaciones posibles de los campos del registro
        permutaciones = list(itertools.permutations(tipo.tipos))
        valores = []

        for permutacion in permutaciones:
            # Se asigna la permutacion actual al tipo            
            tipo.tipos = permutacion

            # se calcula el espacio ocupado y desperdicio de la permitacion actual
            size = 0
            desperdicio = 0
            (sizeAct, desperdicioAct) = (0, 0)
            for tipoActual in tipo.tipos:
                (sizeAct, desperdicioAct) = reordenar(obtenerTipo(tipoActual))
                size += sizeAct
                desperdicio += desperdicioAct

            # Se guardan los valores obtenidos para la permutacion actual en la lista de valores
            valores.append((size, desperdicio))

        # Se retorna la tupla con menor memoria ocupada
        return min(valores)

def obtenerEspacio(objeto):

    # Si se trata de un tipo atomico se devuelve su atributo representacion
    # Si se trata de un struct se devuelve la suma de las representaciones de todos sus tipos
    # Si se trata de un tipo union, se devuelve el valor de representacion mayor
    if isinstance(objeto,Struct):
        acc = 0
        for tipo in objeto.tipos:
            acc+=dicTipos.get(tipo).representacion
        return acc
    elif isinstance(objeto,Union):
        lista = []
        for tipo in objeto.tipos:
            atom = dicTipos.get(tipo)
            lista.append(atom.representacion)
        return max(lista)
    else:
        return objeto.representacion

# metodo que retorna el tipo del objeto asociado al nombre suministrado   
def obtenerTipo(nombre):

    if dicTipos.get(nombre):
        return dicTipos[nombre]
    elif dicStruct.get(nombre):
        return dicStruct[nombre]
    elif dicUnion.get(nombre):
        return dicUnion[nombre]
    else:
        print(f"{nombre} no se encuentra definido")
        return None

# Metodo para calcular el mcm de una lista
# Se utiliza para hallar la alineacion de objetos tipo Union
def mcm_lista(lista):
    if len(lista) == 1:
        return lista[0]
    i = 1
    minimo = mcm(lista[0],lista[1])
    while i < len(lista)-1:
        minimo = mcm(minimo,lista[i+1])
        i += 1
    return minimo

def MCD(a, b):
    temporal = 0
    while b != 0:
        temporal = b
        b = a % b
        a = temporal
    return a

def mcm(a, b):
    return (a * b) / MCD(a, b)

def obtenerAlineacion(tipo) -> int:

    if isinstance(tipo, Atomo):
        # La alineacion de un atomo es su atributo alineacion
        return tipo.alineacion
    elif isinstance(tipo, Union):
        # la alineacion de un tipo Union es el mcm entre sus alineaciones
        tipos = tipo.tipos
        listaTipos = []
        for elem in tipos:
            listaTipos.append(dicTipos[elem].alineacion)
        return int(mcm_lista(listaTipos))
    else:
        # la alineacion de un struct es la alineacion de su primer tipo atomo almacenado
        tipos = tipo.tipos
        return dicTipos[tipos[0]].alineacion

"""
def obtenerDesperdicio(index, alineacion):
    desperdicio = alineacion - index % alineacion
    if index % alineacion != 0:
        return desperdicio
    else:
        return 0
"""
#agregarTipo("int",4,4)
#agregarTipo("char",1,2)
#agregarTipo("bool",1,3)
#agregarStruct("hola","int","char","bool")
#agregarUnion("chao","char","bool")
#describir("hola")
