import TP2_VISUAL as vis

def opciones(numeros_permitidos :list) -> int:
    """
    Pre: Recibe una lista con los posibles numeros que puede tomar nuestra opcion.
    Post: Devuelve un entero que sigue los limites marcados.
    """
    opcion_correcta :bool = False
    while not opcion_correcta:
        opcion :str = input("Ingrese una opcion: ")
        if opcion.isnumeric():
            if int(opcion) in numeros_permitidos:
                opcion_correcta :bool = True
            else: print("   Ingrese un numero dentro de las opciones.")
        else: print("   Ingrese un numero.")
    return int(opcion)

def main() -> None:
    vis.inicio()
    terminar :bool = False
    while not terminar:
        print(vis.MENU)
        opcion :int = opciones(range(1,9))
        if opcion == 1:
            pass
        elif opcion == 8:
            terminar :bool = True
            
main()