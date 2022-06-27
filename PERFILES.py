import tekore as tk
from webbrowser import open as web_open
import TP2_VISUAL as vis
import os
import csv

ID_CLIENTE: str = "176365611325455e8059fbd545371d89"
CLIENTE_SECRETO: str = "ed35a90b681042f4bbad9f284383c88a"
URI_REDIRECCION: str = "http://localhost:8888/callback"
SCOPE = tk.scope.every

def opciones(numeros_permitidos: list) -> int:
    """
    Pre: Recibe una lista con los posibles numeros que puede tomar nuestra opcion.
    Post: Devuelve un entero que sigue los limites marcados.
    """
    opcion_correcta: bool = False
    while not opcion_correcta:
        opcion: str = input("Ingrese una opcion: ")
        if opcion.isnumeric():
            if int(opcion) in numeros_permitidos:
                opcion_correcta: bool = True
            else: print("   Ingrese un numero dentro de las opciones.")
        else: print("   Ingrese un numero.")
    return int(opcion)


def autenticar_spotify() -> str:
    refresh_token: str = ""
    credenciales: tk.RefreshingCredentials = tk.RefreshingCredentials(ID_CLIENTE, CLIENTE_SECRETO, URI_REDIRECCION)
    auth = tk.UserAuth(credenciales, SCOPE) # FALTA TYPING
    print(vis.INSTRUCCIONES)
    input("Presione Enter para que se abra Spotify: ")
    web_open(auth.url)
    print()
    print("Aqui abajo debes ingresar la URL que copiaste:  ")
    url :str = input("--->  ").strip()
    try:
        token: tk.RefreshingToken = auth.request_token(url=url)
    except KeyError:
        print(vis.ERROR_URL)
    else:
        refresh_token: str = token.refresh_token
        print(vis.DATOS_GUARDADOS)
    return refresh_token


def guardar_perfil(nombre:str, refresh_token: str = "", youtube: str = "") -> None:
    with open("perfiles_datos.csv", "a", newline="", encoding="UTF-8") as archivo_csv:
        csv_writer = csv.writer(archivo_csv, delimiter=",", quotechar='"')
        if os.stat("perfiles_datos.csv").st_size == 0:
            csv_writer.writerow(["Nombre Perfil", "Refresh Token", "Cosa de Youtube"])
        csv_writer.writerow([nombre, refresh_token, youtube])

def nombres_perfiles_guardados() -> list:
    nombres_perfiles: list = []
    try:
        archivo_csv = open("perfiles_datos.csv", newline="", encoding="UTF-8")
    except FileNotFoundError:
        return nombres_perfiles
    else:
        csv_reader = csv.reader(archivo_csv, delimiter=",")
        next(csv_reader)
        for linea in csv_reader:
            nombres_perfiles.append(linea[0])
        archivo_csv.close()
    return nombres_perfiles

def nombre_perfil() -> str:
    nombre_disponible: bool = False
    nombres_usados: list = nombres_perfiles_guardados()
    while not nombre_disponible:
        nombre: str = input("Ingresa el nombre del perfil: ")
        if not nombres_usados:
            nombre_disponible: bool = True
        elif nombre and (nombre not in nombres_usados):
            nombre_disponible: bool = True
        else:
            print(vis.NOMBRE_NO_VALIDO)
            print(" Intentalo de nuevo.")
    return nombre

def nuevo_perfil():
    nombre: str = nombre_perfil()
    opciones_elegidas: list = []
    terminar: bool = False
    while not terminar:
        vis.youtube_spotify(True, opciones_elegidas)
        opcion: int = opciones([1, 2, 3])
        if opcion == 1:
            pass # AQUI VA LA PARTE DE YOUTUBE
        elif opcion == 2:
            refresh_token: str = autenticar_spotify()
            if refresh_token:
                opciones_elegidas.append(opcion)   #REVISAR EL APPEND, QUE PASA SI EL USUARIO USA ESTO 2 VECES
        elif opcion == 3 and opciones_elegidas:
            guardar_perfil(nombre, refresh_token)
            print(vis.DATOS_GUARDADOS)
            terminar: bool = True
        else:
            terminar: bool = True

def elegir_perfil(perfil: dict) -> str:
    perfil_elegido: str = ""
    nombres_perfiles: list = nombres_perfiles_guardados()
    nombres_perfiles.append("NO ELEGIR PERFIL")
    if len(nombres_perfiles) == 1:
        print(vis.NO_PERFILES)
        return perfil_elegido
    vis.visual_lista_elementos(nombres_perfiles, "Perfiles Guardados", True)
    numeros_permitidos: list = [x for x in range(1,len(nombres_perfiles)+1)]
    opcion: int = opciones(numeros_permitidos)
    if opcion == len(nombres_perfiles):
        return perfil_elegido
    if perfil["nombre"] and perfil["nombre"] == nombres_perfiles[opcion-1]:   # CUANDO VUELVE A ELEGIR PERFIL, PARA QUE NO ELIJA EL MISMO
        return perfil_elegido
    perfil_elegido: str = nombres_perfiles[opcion-1]
    return perfil_elegido

def manejo_perfiles(perfil: dict):
    terminar: bool = False
    while not terminar:
        vis.menu_perfiles(perfil["nombre"])
        opcion: int = opciones([1, 2, 3])
        if opcion == 1:
            perfil_elegido: str = elegir_perfil(perfil)                             #EN REVISION
            if perfil_elegido:
                perfil["nombre"] = perfil_elegido
        elif opcion == 2:
            nuevo_perfil()
        else:
            terminar: bool = True

def datos_por_indice(indice: int) -> list:
    archivo_csv = open("perfiles_datos.csv", newline="", encoding="UTF-8")
    csv_reader = csv.reader(archivo_csv, delimiter=",")   #FALTA UN TRY/EXCEPT?
    for x in range(indice+1):
        next(csv_reader)
    datos :list = next(csv_reader)
    return datos

def conseguir_datos_playlists(spotify, id_usuario):
    datos = []
    datos_playlists = spotify.playlists(id_usuario)
    for playlist in datos_playlists.items:
        diccionario = {}
        diccionario["name"] = playlist.name
        diccionario["id"] = playlist.id
        diccionario["collaborative"] = playlist.collaborative
        diccionario["description"] = playlist.description
        """
        canciones = []
        for cancion in spotify.playlist_items(playlist.id).items:
            canciones.append(cancion.track.name)
        diccionario["tracks"] = canciones
        """
        datos.append(diccionario)
    return datos


def datos_necesarios_perfil(perfil: dict) -> None:
    nombres_usados: list = nombres_perfiles_guardados()
    indice_datos: int = nombres_usados.index(perfil["nombre"])
    datos_perfil: list = datos_por_indice(indice_datos)
    if datos_perfil[1]:
        token = tk.refresh_user_token(ID_CLIENTE, CLIENTE_SECRETO, datos_perfil[1])
        spotify = tk.Spotify(token)
        perfil["spotify"] = spotify
    if "spotify" in perfil:
        id_usuario = spotify.current_user().id
        perfil["id_usuario_spotify"] = id_usuario
    if "spotify" in perfil and "id_usuario_spotify" in perfil:
        datos_playlists: list = conseguir_datos_playlists(perfil["spotify"], perfil["id_usuario_spotify"])
        perfil["playlists_spotify"] = datos_playlists

def datos_agregados_correctamente(perfil: dict) -> bool:
    if not perfil["nombre"]:
        return False
    datos_necesarios_perfil(perfil)
    if "spotify" not in perfil:
        return False
    elif "id_usuario_spotify" not in perfil:
        return False
    elif "playlists_spotify" not in perfil:
        return False
    return True
