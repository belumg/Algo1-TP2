import tekore as tk
from webbrowser import open as web_open
import TP2_VISUAL as vis

ID_CLIENTE: str = "ea4916f2e2d144a992b0f2d7bed6c25d"
CLIENTE_SECRETO: str = "54833ae03ee847c385cd918d869b1052"
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
    datos_guardar: tuple = (ID_CLIENTE, CLIENTE_SECRETO, URI_REDIRECCION, refresh_token)
    tk.config_to_file("cuentas_spotify.txt", datos_guardar, nombre_perfil)
    
def nuevo_perfil_spotify(nombre_perfil) -> None:
    """Permite que el usuario inicie sesion y de permisos y luego guarda sus datos en un archivo."""
    credenciales: tk.RefreshingCredentials = tk.RefreshingCredentials(ID_CLIENTE, CLIENTE_SECRETO, URI_REDIRECCION)
    auth = tk.UserAuth(credenciales, SCOPE)
    print(vis.INSTRUCCIONES)
    input("Presione Enter para que se abra Spotify: ")
    web_open(auth.url)
    print()
    print("Aqui abajo debes ingresar la URL que copiaste:  ")
    url :str = input("--->  ").strip()
    token_usuario: tk.RefreshingToken = auth.request_token(url=url)
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
    perfil_elegido: str = ""
    while not terminar:
        vis.menu_perfiles(perfil_elegido)
        opcion: int = opciones([1, 2, 3])
        if opcion == 1:
            perfil: str = elegir_perfil()
            if perfil != "no_eligio_perfil":
                perfil_elegido: str = perfil
        elif opcion == 2:
            nuevo_perfil()
        else:
            terminar: bool = True
    return perfil_elegido

def conseguir_id_usuario(spotify):
    datos_usuario = spotify.current_user()
    return datos_usuario.id

def playlists_spotify(spotify, id_usuario) -> None:
    datos_playlists = spotify.playlists(id_usuario)
    nombres = [x.name for x in datos_playlists.items]
    if nombres:
        vis.visual_lista_elementos(nombres, "Playlists de Spotify", True)
    else:
        print(vis.NO_PLAYLIST)

def main() -> None:
    vis.inicio()
    perfil: str = manejo_perfiles()
    if perfil:
        datos_usuario: tuple = tk.config_from_file("cuentas_spotify.txt", perfil, True)
        token = tk.refresh_user_token(*datos_usuario[:2], datos_usuario[3])
        spotify = tk.Spotify(token)
        id_usuario = conseguir_id_usuario(spotify)
        terminar: bool = False
        while not terminar:
            vis.menu_opciones()
            opcion: int = opciones([1, 2, 3, 4, 5, 6, 7, 8])
            if opcion == 1:
                playlists_spotify(spotify, id_usuario)
            elif opcion == 2:
                print(token.is_expiring)
                print(token.expires_in)
                print(token.expires_at)
            elif opcion == 3:
                pass
            elif opcion == 8:
                terminar: bool = True
        
main()
