import tekore as tk
from webbrowser import open as web_open
import TP2_VISUAL as vis

ID_CLIENTE: str = "ea4916f2e2d144a992b0f2d7bed6c25d"
URI_REDIRECCION: str = "http://localhost:8888/callback"
SCOPE = tk.scope.every

def opciones(numeros_permitidos :list) -> int:
    """
    Pre: Recibe una lista con los posibles numeros que puede tomar nuestra opcion.
    Post: Devuelve un entero que sigue los limites marcados.
    """
    opcion_correcta: bool = False
    while not opcion_correcta:
        opcion: str = input("Ingrese una opcion: ")
        if opcion.isnumeric():
            if int(opcion) in numeros_permitidos:
                opcion_correcta :bool = True
            else: print("   Ingrese un numero dentro de las opciones.")
        else: print("   Ingrese un numero.")
    return int(opcion)

def guardar_nuevo_perfil(refresh_token, nombre_perfil) -> None:
    datos_guardar: tuple = (ID_CLIENTE, None, URI_REDIRECCION, refresh_token)
    tk.config_to_file("cuentas_spotify.txt", datos_guardar, nombre_perfil)
    
def nuevo_perfil_spotify(nombre_perfil) -> None:
    """Permite que el usuario inicie sesion y de permisos y luego guarda sus datos en un archivo."""
    credenciales: tk.RefreshingCredentials = tk.RefreshingCredentials(ID_CLIENTE, redirect_uri=URI_REDIRECCION)
    url, verificador = credenciales.pkce_user_authorisation(SCOPE)
    print(vis.INSTRUCCIONES)
    input("Presione Enter para que se abra Spotify: ")
    web_open(url)
    print()
    print("Aqui abajo debes ingresar la URL que copiaste:  ")
    url :str = input("--->  ").strip()
    codigo: str= tk.parse_code_from_url(url)
    token_usuario: tk.RefreshingToken = credenciales.request_pkce_token(codigo, verificador)
    refresh_token: str = token_usuario.refresh_token
    guardar_nuevo_perfil(refresh_token, nombre_perfil)
    print(vis.DATOS_GUARDADOS)

def nuevo_perfil():
    nombre: str = input("Ingrese el nombre del perfil: ")
    vis.youtube_spotify()
    opcion: int = opciones([1, 2])
    if opcion == 1:
        pass
    else:
        nuevo_perfil_spotify(nombre)
    with open("nombres_perfiles.txt", "a") as f:
        f.write(nombre+"\n")

def perfiles_guardados() -> list:
    """
    Devuelve una lista con los nombres de los perfiles guardados que saca de un archivo,
    si no encuentra ese archivo entonces devuelve una lista vacia.
    """
    nombres_perfiles: list = []
    try:
        archivo = open("nombres_perfiles.txt", "r")
    except FileNotFoundError:
        print(vis.NO_PERFILES)
    else:
        for linea in archivo:
            nombres_perfiles.append(linea.rstrip())
        archivo.close()
    finally:
        return nombres_perfiles

def elegir_perfil() -> str:
    nombres_perfiles: list = perfiles_guardados()
    if nombres_perfiles:
        vis.visual_lista_elementos(nombres_perfiles, "Perfiles Guardados", True)
        numeros_permitidos: list = [x for x in range(1,len(nombres_perfiles)+1)]
        opcion: int = opciones(numeros_permitidos)
        return nombres_perfiles[opcion-1]
    else:
        return "no_eligio_perfil"

def manejo_perfiles():
    terminar: bool = False
    eligio_perfil: bool = False
    while not terminar:
        vis.menu_perfiles(eligio_perfil)
        opcion: int = opciones([1, 2, 3])
        if opcion == 1:
            perfil: str = elegir_perfil()
            if perfil != "no_eligio_perfil":
                eligio_perfil: bool = True
        elif opcion == 2:
            nuevo_perfil()
        else:
            terminar: bool = True
    if eligio_perfil:
        return perfil
    else:
        return "no_eligio_perfil"

def main() -> None:
    vis.inicio()
    perfil: str = manejo_perfiles()
    if perfil != "no_eligio_perfil":
        datos_usuario: tuple = tk.config_from_file("cuentas_spotify.txt", perfil, True)
        token = tk.refresh_pkce_token(datos_usuario[0], datos_usuario[3])
        print(token)
        terminar: bool = False
        while not terminar:
            vis.menu_opciones()
            opcion: int = opciones([1, 2, 3, 4, 5, 6, 7, 8])
            if opcion == 1:
                pass
            elif opcion == 2:
                pass
            elif opcion == 8:
                terminar: bool = True
        
main()
