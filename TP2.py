import tekore as tk
import TP2_VISUAL as vis
import AUTENTICACION as aut

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

def nuevo_perfil():
    nombre: str = input("Ingrese el nombre del perfil: ")
    vis.youtube_spotify()
    opcion: int = opciones([1, 2])
    if opcion == 1:
        pass
    else:
        aut.nuevo_perfil_spotify(nombre)
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

def elegir_perfil(perfil:list) -> None:
    """
    Pre: Recibe una lista perfil que puede estar vacia o contener un solo elemento.
    Post: Si hay perfiles guardados entonces modifica la lista perfil, caso contrario no hace nada.
    """
    nombres_perfiles: list = perfiles_guardados()
    if nombres_perfiles:
        vis.visual_lista_elementos(nombres_perfiles, "Perfiles Guardados", True)
        numeros_permitidos: list = [x for x in range(1,len(nombres_perfiles)+1)]
        opcion: int = opciones(numeros_permitidos)
        if perfil: 
            perfil[0] = nombres_perfiles[opcion-1]
        else: 
            perfil.append(nombres_perfiles[opcion-1])

def manejo_perfiles(perfil:list) -> None:
    terminar: bool = False
    while not terminar:
        vis.menu_perfiles(perfil)
        opcion: int = opciones([1, 2, 3])
        if opcion == 1:
            elegir_perfil(perfil)
        elif opcion == 2:
            nuevo_perfil()
        else:
            terminar: bool = True

def conseguir_id_usuario(spotify):
    datos_usuario = spotify.current_user()
    return datos_usuario.id

def playlists_spotify(spotify, id_usuario) -> None:
    datos_playlists = spotify.playlists(id_usuario)
    nombres = [x.name for x in datos_playlists.items]
    #id_playlist = [x.id for x in datos_playlists.items]
    if nombres:
        vis.visual_lista_elementos(nombres, "Playlists de Spotify", True)
        """
        for id in id_playlist:          #PARA LISTAR LOS NOMBRES DE LAS CANCIONES.
            for cancion in spotify.playlist_items(id).items:
                print(cancion.track.name)
        """
    else:
        print(vis.NO_PLAYLIST)

def datos_necesarios_perfil(perfil:list) -> tuple:
    datos_usuario: tuple = tk.config_from_file("cuentas_spotify.txt", perfil[0], True)
    token = tk.refresh_user_token(*datos_usuario[:2], datos_usuario[3])
    spotify = tk.Spotify(token)
    id_usuario = conseguir_id_usuario(spotify)
    return token, spotify, id_usuario

def main() -> None:
    vis.inicio()
    perfil: list = []
    manejo_perfiles(perfil)
    if perfil:
        token, spotify, id_usuario = datos_necesarios_perfil(perfil)
        terminar: bool = False
        while not terminar:
            vis.menu_opciones()
            opcion: int = opciones([1, 2, 3, 4, 5, 6, 7, 8])
            if opcion == 1:
                playlists_spotify(spotify, id_usuario)
            elif opcion == 2:
                pass
            elif opcion == 3:
                pass
            elif opcion == 7:
                manejo_perfiles(perfil)
            elif opcion == 8:
                terminar: bool = True
        
main()
