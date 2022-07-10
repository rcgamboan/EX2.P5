import manejador
import sys

# cliente que usa las funciones definidas en eval y mostrar
# para trabajar con expresiones booleanas

print("\n\nManejador de tipos de datos")
print("\nA continuacion indique la operacion que quiere realizar")
print("\nLas operaciones disponibles son las siguientes: ")
print("\nATOMICO   <nombre> <representación> <alineación> Deﬁne un nuevo tipo atómico de nombre <nombre>, que ocupa <representación> bytes y esta alineado a <alineación> bytes.")
print("\nSTRUCT    <nombre> [<tipo>] Deﬁne un nuevo registro de nombre <nombre> y los tipos definidos en [tipos]")
print("\nUNION     <nombre> [<tipo>] Deﬁne un nuevo registro variante de nombre <nombre> y los tipos definidos en [tipos]")
print("\nDESCRIBIR <nombre> Debe dar la información correspondiente al tipo con nombre <nombre>")

print("\nSALIR                         Termina la ejecucion del programa\n")
while True:

    comando = input("main> ")

    if comando == '':
        continue

    argumentos = comando.split()

    if argumentos[0] == "SALIR" or argumentos[0] == "salir":
        print("Se termina la ejecucion del programa")
        sys.exit()
    elif argumentos[0] == "ATOMICO":
        
        if len(argumentos) < 4:
            print("Formato invalido.")
        else:
            nombre = argumentos[1]
            representacion = int(argumentos[2])
            alineacion = int(argumentos[3])
            
            manejador.agregarTipo(nombre,representacion,alineacion)
            
            
    elif argumentos[0] == "STRUCT":

        if len(argumentos) < 3:
            print("Formato invalido.")
        else:
            nombre = argumentos[1]
            tipos = argumentos[2:]
            manejador.agregarStruct(nombre,tipos)

    elif argumentos[0] == "UNION":

        if len(argumentos) < 3:
            print("Formato invalido.")
        else:
            nombre = argumentos[1]
            tipos = argumentos[2:]
            manejador.agregarUnion(nombre,tipos)
    
    elif argumentos[0] == "DESCRIBIR":

        if len(argumentos) != 2:
            print("Formato invalido.")
        else:
            nombre = argumentos[1]
            manejador.describir(nombre)
                
            
    else:
        print("Operacion no valida\n")
