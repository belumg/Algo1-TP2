from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from webbrowser import open as web_open
import tekore as tk
import os
import json
import TP2_VISUAL as vis

SCOPE: tk.Scope = tk.scope.every

####################################################################################################
####################################################################################################

def input_num_con_control(min:int, max:int) -> int:
    """Devuelve un entero que esta entre los numeros recibidos por parametro."""
    seleccion: str = input("      >>>    ")
    while not seleccion.isnumeric() or int(seleccion) > max or int(seleccion) < min:
        seleccion: str = input("Inválido. Vuelva a ingresar >>>  ")
    return int(seleccion)

def input_con_control(palabras_permitidas: list, mensaje: str) -> str:
    """Devuelve un string que se encuentra entre las palabras permitidas."""
    print(mensaje)
    seleccion: str = input("      >>>    ").lower()
    while seleccion not in palabras_permitidas:
        seleccion: str = input("Inválido. Vuelva a ingresar >>>  ").lower()
    return seleccion

######################### AUTENTICAR SPOTIFY #######################################################
####################################################################################################

def autenticar_spotify(credenciales_SP: tuple) -> str:
    """Devuelve un refresh_token si la autenticacion salio bien, caso contrario devuelve un string vacio."""
    refresh_token: str = ""
    credenciales: tk.RefreshingCredentials = tk.RefreshingCredentials(credenciales_SP[0], credenciales_SP[1], credenciales_SP[2])
    auth: tk.UserAuth = tk.UserAuth(credenciales, SCOPE)
    print(vis.INSTRUCCIONES)
    input("Presione Enter para que se abra Spotify: ")
    web_open(auth.url)
    print()
    print("Aqui abajo debes ingresar la URL que copiaste:  ")
    url: str = input("--->  ").strip()
    try:
        token: tk.RefreshingToken = auth.request_token(url=url)
    except:
        print(vis.ERROR_URL)
    else:
        refresh_token: str = token.refresh_token
        print(vis.DATOS_GUARDADOS)
    return refresh_token

######################### AUTENTICAR YOUTUBE #######################################################
####################################################################################################

def autenticarYT() -> object:   # REVISAR, DEVUELVE STRING CUANDO FALLA
    permisos = ""
    scopes = ["https://www.googleapis.com/auth/youtube"]

    # Verificación HTTPS OAuthlib activada.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name: str = "youtube"
    api_version: str = "v3"
    client_secrets_file: str = "credenciales_YT.json"

    # Autorización.
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    try:
        permisos = flow.run_console()
    except:
        print(vis.ERROR_URL)
    else:
        # Creo un cliente API para hacer solicitudes.
        clienteYT: object = build(api_service_name, api_version, credentials=permisos)
    return permisos

######################### GUARDAR INFORMACION EN JSON ##############################################
####################################################################################################

def escribir_json(datos, nombre_archivo):
    """Crea, si aun no existe, un archivo json con el nombre y los datos dados por parametro."""
    with open(nombre_archivo, "w") as f:
        json.dump(datos, f, indent=3)


def sacar_info_json(nombre_archivo) -> dict:
    """Devuelve toda la informacion que hay en el archivo json."""
    with open(nombre_archivo) as f:
        datos_del_archivo = json.load(f)
    return datos_del_archivo


def guardar_datos_en_json(usuario: str, refresh_token: str, permisos) -> None:
    """Guarda los datos recibidos en un archivo json (si no existe, se crea aqui)."""
    datos_existentes: dict = {}
    datos_guardar: dict = {usuario: {"spotify": refresh_token, "youtube": json.loads(permisos.to_json())}}
    if os.path.isfile("datos_perfiles.json"):
        datos_existentes: dict = sacar_info_json("datos_perfiles.json")
    datos_existentes.update(datos_guardar)
    escribir_json(datos_existentes, "datos_perfiles.json")

######################### CREAR NUEVO PERFIL #######################################################
####################################################################################################

def nombre_perfil() -> str:
    """Le pide un nombre al usuario y, si ese nombre no es un string vacio o ya existe, lo devuelve."""
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


def nuevo_perfil(credenciales_SP: tuple):
    """Guarda el perfil solo si acepto los permisos de al menos una plataforma."""
    nombre: str = nombre_perfil()
    opciones_elegidas: list = []
    terminar: bool = False
    while not terminar:
        vis.youtube_spotify(True, opciones_elegidas)
        opcion = input_num_con_control(1,3)
        if opcion == 1:
            obj_youtube = autenticarYT()
            if obj_youtube:
                opciones_elegidas.append(opcion)
        elif opcion == 2:
            refresh_token: str = autenticar_spotify(credenciales_SP)
            if refresh_token:
                opciones_elegidas.append(opcion)
        elif opcion == 3 and opciones_elegidas and (1 not in opciones_elegidas or 2 not in opciones_elegidas):
            if 1 not in opciones_elegidas: falta: str = "Youtube"
            else: falta: str = "Spotify"
            vis.falta_plataforma(falta)
        elif opcion == 3 and opciones_elegidas:
            guardar_datos_en_json(nombre, refresh_token, obj_youtube)
            print(vis.DATOS_GUARDADOS)
            terminar: bool = True
        else:
            terminar: bool = True

######################### ELEGIR PERFIL ############################################################
####################################################################################################

def nombres_perfiles_guardados() -> list:
    """Devuelve los nombres que estan el archivo json de los perfiles, si no lo encuentra devuelve una lista vacia."""
    if not os.path.isfile("datos_perfiles.json"):
        return []
    with open("datos_perfiles.json") as f:
        datos = json.load(f)
        return list(datos.keys())


def elegir_perfil(perfil: dict) -> str:
    """
    Pre: Recibe un diccionario con los datos del perfil actual.
    Post: Se le imprime un lista de perfiles y devuelve un string con el perfil elegido.
          Si no eligio, no hubo perfiles para elegir o si eligio el perfil actual entonces devuelve un string vacio.
    """
    perfil_elegido: str = ""
    nombres_perfiles: list = nombres_perfiles_guardados()
    nombres_perfiles.append("NO ELEGIR PERFIL")
    if len(nombres_perfiles) == 1:
        print(vis.NO_PERFILES)
        return perfil_elegido
    vis.visual_lista_elementos(nombres_perfiles, "Perfiles Guardados", True)
    opcion = input_num_con_control(1,len(nombres_perfiles))
    if opcion == len(nombres_perfiles):
        return perfil_elegido
    if perfil["username"] and perfil["username"] == nombres_perfiles[opcion-1]:   # Para que no elija el mismo perfil cuando hace el cambio de perfil.
        return perfil_elegido
    perfil_elegido: str = nombres_perfiles[opcion-1]
    return perfil_elegido

####################################################################################################
####################################################################################################

def manejo_perfiles(perfil: dict, credenciales_SP: tuple):
    """
    Genera un menu para crear y guardar perfiles junto con la opcion de elegir uno de los perfiles guardados.
    Si eligio un perfil entonces el nombre se guardara en el diccionario recibido.
    """
    terminar: bool = False
    while not terminar:
        vis.menu_perfiles(perfil["username"])
        opcion = input_num_con_control(1,3)
        if opcion == 1:
            perfil_elegido: str = elegir_perfil(perfil)                             # EN REVISION
            if perfil_elegido:
                if perfil["username"]: perfil.clear()
                perfil["username"] = perfil_elegido
        elif opcion == 2:
            nuevo_perfil(credenciales_SP)
        else:
            terminar: bool = True

######################### YOUTUBE: VALIDACION DE PERMISOS ##########################################
####################################################################################################

def validar_permisosYT(usuario: str) -> object:

    datos: dict = sacar_info_json("datos_perfiles.json")

    # Me guardo las claves que generó el usuario del perfil para YouTube.
    claves: dict = datos[usuario]["youtube"]

    # Recupero los permisos.
    permisos = Credentials(
        token=claves["token"], refresh_token=claves["refresh_token"],
        token_uri=claves["token_uri"], client_id=claves["client_id"],
        client_secret=claves["client_secret"], scopes=claves["scopes"]
    )

    # Verifico si son válidos.
    if (permisos.expired == False):
        # Solicito nuevos permisos y refresco los existentes.
        solicitar = Request()
        permisos.refresh(solicitar)

        # Los guardo en el archivo de credenciales de perfiles.
        datos[usuario]["youtube"] = json.loads(permisos.to_json())
        escribir_json(datos, "datos_perfiles.json")

        # Genero un nuevo cliente de YouTube.
        api_service_name: str = "youtube"
        api_version: str = "v3"
        youtube: object = build(api_service_name, api_version, credentials=permisos)

        return youtube
    else:
        return youtube

######################### OBTENCION DE DATOS #######################################################
####################################################################################################

def obtener_refresh_token_perfil(nombre: str) -> str:
    """Devuelve el refresh_token del nombre recibido, si el archivo de donde lo saca no esta entonces devuelve un str vacio."""
    if not os.path.isfile("datos_perfiles.json"):
        return ""
    with open("datos_perfiles.json") as f:
        datos = json.load(f)
    return datos[nombre]["spotify"]


def listar_playlistsYT(youtube: object) -> dict:
    request = youtube.playlists().list(
                    part="snippet,id",
                    maxResults=50,
                    mine=True
                    )
    response = request.execute()

    # Agrega nombre de playlist fuera de snippet >>>>>>>>>>>>>>>>>>>>>>
    for playlist in response['items']:
        playlist['name'] = playlist['snippet']['title']
    return response['items']


def datos_playlists_SP(spotify, id_usuario):
    """
    Pre: Recibe un objeto spotify (ya con los datos de nuestro perfil elegido) y el id de Spotify del perfil actual.
    Post: Devuelve una lista con un monton de datos de las playlists que tiene el perfil actual.
    """
    datos = []
    datos_playlists = probando(spotify.playlists, [id_usuario])  # Que pasa si el usuario no tiene playlists?
    if not datos_playlists:
        return datos
    for playlist in datos_playlists.items:
        datos_playlist: dict = {}
        datos_playlist["name"] = playlist.name
        datos_playlist["id"] = playlist.id
        datos_playlist["collaborative"] = playlist.collaborative
        datos_playlist["description"] = playlist.description
        """
        canciones = []
        for cancion in spotify.playlist_items(playlist.id).items:
            canciones.append(cancion.track.name)
        diccionario["tracks"] = canciones
        """
        datos.append(datos_playlist)
    return datos

######################### AGREGARLE DATOS AL PERFIL ################################################
####################################################################################################

def probando(funcion_a_probar, datos_que_necesita: list = []):
    """
    Pre: Recibe una funcion junto con una lista de sus argumentos.
    Post: Devuelve un string vacio si el usuario dejo de intentar que su funcion, bueno, funcionara.
    """
    terminar: bool = False
    dato_buscado = ""
    while not terminar:
        try:
            if datos_que_necesita:
                dato_buscado = funcion_a_probar(*datos_que_necesita)
            else:
                dato_buscado = funcion_a_probar()
        except:
            print(vis.NO_INTERNET)
            print(" Necesitamos internet para acceder a los datos de su perfil.")
            intentar: str = input_con_control(["si", "no"], "Desea intentarlo de nuevo(si/no)?  ")
            if intentar == "no":
                terminar: bool = True
        else:
            terminar: bool = True
    return dato_buscado

def datos_necesarios_perfil(perfil: dict, credenciales_SP: tuple) -> None:
    """Le agrega datos sobre las plataformas al perfil recibido."""
    # Spotify:
    refresh_token = obtener_refresh_token_perfil(perfil["username"])
    if refresh_token:
        print("Consiguiendo datos de Spotify...")
        datos_necesarios: list = [credenciales_SP[0], credenciales_SP[1], refresh_token] 
        token = probando(tk.refresh_user_token, datos_necesarios)
        if token:
            spotify = tk.Spotify(token)
            perfil["spotify"] = spotify
    if "spotify" in perfil:
        id_usuario: str = probando(spotify.current_user)
        if id_usuario:
            perfil["id_usuario_spotify"] = id_usuario.id
    if "spotify" in perfil and "id_usuario_spotify" in perfil:
        datos_playlists: list = datos_playlists_SP(perfil["spotify"], perfil["id_usuario_spotify"])
        if datos_playlists:
            perfil["playlists_spotify"] = datos_playlists

    # Youtube:
    print("Consiguiendo datos de Youtube...")
    youtube = validar_permisosYT(perfil["username"])
    perfil["youtube"] = youtube
    if "youtube" in perfil:
        request = youtube.channels().list(
            part= "id",
            mine= True
            )
        response = request.execute()["items"] # Devuelve una lista con la información del canal.
        id_YT: str = response[0]["id"]
        perfil["id_usuario_youtube"] = id_YT
    if "youtube" in perfil and "id_usuario_youtube" in perfil:
        datos_playlists: list = listar_playlistsYT(perfil["youtube"])
        perfil["playlists_youtube"] = datos_playlists

####################################################################################################
####################################################################################################

def datos_agregados_correctamente(usuario_actual: dict, credenciales_SP: tuple) -> bool:
    """
    Pre: Recibe un diccionario con los datos del perfil actual.
    Post: Devuelve un False si encuentra que falta un dato importante.
    """
    if not usuario_actual["username"]:
        return False
    datos_necesarios_perfil(usuario_actual, credenciales_SP)
    if "spotify" not in usuario_actual:
        return False
    elif "id_usuario_spotify" not in usuario_actual:
        return False
    elif "playlists_spotify" not in usuario_actual:
        return False
    elif "youtube" not in usuario_actual:
        return False
    elif "id_usuario_youtube" not in usuario_actual:
        return False
    elif "playlists_youtube" not in usuario_actual:
        return False
    return True
