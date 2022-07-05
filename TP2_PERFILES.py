from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from webbrowser import open as web_open
import tekore as tk
import os
import json
import TP2_VISUAL as vis

####################################################################################################
####################################################################################################

SCOPE: tk.Scope = tk.scope.every

####################################################################################################
####################################################################################################

def input_num_con_control(min:int, max:int) -> int:
    """Devuelve un entero que esta entre los numeros recibidos por parametro."""
    seleccion: str = input("      >>>    ")
    while not seleccion.isnumeric() or int(seleccion) > max or int(seleccion) < min:
        seleccion: str = input("Inválido. Vuelva a ingresar >>>  ")
    return int(seleccion)


def input_con_control(palabras_permitidas: list, mensaje: str, cansancio: int = 100, mensaje_cansancio: str = "") -> str:
    """Devuelve un string que se encuentra entre las palabras permitidas."""
    print(mensaje)
    intentos: int = 0
    seleccion: str = input("      >>>    ").lower()
    while seleccion not in palabras_permitidas:
        if intentos > cansancio:
            print(mensaje_cansancio)
        seleccion: str = input("Inválido. Vuelva a ingresar >>>  ").lower()
        intentos += 1
    return seleccion

######################### AUTENTICAR SPOTIFY #######################################################
####################################################################################################

def autenticar_spotify() -> str:
    """Devuelve un refresh_token si la autenticacion salio bien, caso contrario devuelve un string vacio."""
    refresh_token: str = ""
    credenciales_SP: tuple = tuple(sacar_info_json("credenciales.json")["spotify"].values())
    credenciales: tk.RefreshingCredentials = tk.RefreshingCredentials(*credenciales_SP)
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

def autenticarYT() -> object:  # ERROR: Puede devolver un string o un objeto.
    """ Autentica a un determinado usuario en la plataforma Youtube """
    permisos = ""
    scopes = ["https://www.googleapis.com/auth/youtube"]

    # Verificación HTTPS OAuthlib activada.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name: str = "youtube"
    api_version: str = "v3"
    credenciales_YT: dict = sacar_info_json("credenciales.json")["youtube"] 
    # Autorización.
    flow = InstalledAppFlow.from_client_config(credenciales_YT, scopes)
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

def escribir_json(datos, nombre_archivo) -> None:
    """Crea, si aun no existe, un archivo json con el nombre y los datos dados por parametro."""
    with open(nombre_archivo, "w") as f:
        json.dump(datos, f, indent=3)


def sacar_info_json(nombre_archivo) -> dict:
    """Devuelve toda la informacion que hay en el archivo json."""
    with open(nombre_archivo) as f:
        datos_del_archivo: dict = json.load(f)
    return datos_del_archivo


def guardar_datos_en_json(usuario: str, refresh_token: str, permisos) -> None:      # Falta typing de permisos
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


def nuevo_perfil() -> None:
    """Guarda el perfil solo si acepto los permisos de al menos una plataforma."""
    nombre: str = nombre_perfil()
    opciones_elegidas: list = []
    terminar: bool = False
    while not terminar:
        vis.youtube_spotify(True, opciones_elegidas)
        opcion: int = input_num_con_control(1,3)
        if opcion == 1:
            obj_youtube = autenticarYT()  # Falta typing
            if obj_youtube:
                opciones_elegidas.append(opcion)
        elif opcion == 2:
            refresh_token: str = autenticar_spotify()
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
    nombres_perfiles: list = []
    if os.path.isfile("datos_perfiles.json"):
        datos: dict = sacar_info_json("datos_perfiles.json")
        nombres_perfiles: list = list(datos.keys())
    return nombres_perfiles


def elegir_perfil(perfil: dict) -> str:
    """
    Pre: Recibe un diccionario con los datos del perfil actual.
    Post: Se le imprime un lista de perfiles y devuelve un string con el perfil elegido.
          Si no eligio, no hubo perfiles para elegir o si eligio el perfil actual entonces devuelve un string vacio.
    """
    nombres_perfiles: list = nombres_perfiles_guardados()
    nombres_perfiles.append("NO ELEGIR PERFIL")
    if not len(nombres_perfiles) == 1:
        vis.visual_lista_elementos(nombres_perfiles, "Perfiles Guardados", True)
        opcion: int = input_num_con_control(1,len(nombres_perfiles))
        if (opcion == len(nombres_perfiles) or
            (perfil["username"] and
            perfil["username"] == nombres_perfiles[opcion-1])):
            # Si la opcion elegida es salir o volvio a elegir el mismo perfil.
            perfil_elegido: str = ""
        else:
            perfil_elegido: str = nombres_perfiles[opcion-1]
    else:
        perfil_elegido: str = ""
        print(vis.NO_PERFILES)
    return perfil_elegido

####################################################################################################
####################################################################################################

def manejo_perfiles(perfil: dict) -> None:
    """
    Genera un menu para crear y guardar perfiles junto con la opcion de elegir uno de los perfiles guardados.
    Si eligio un perfil entonces el nombre se guardara en el diccionario recibido.
    """
    terminar: bool = False
    while not terminar:
        vis.menu_perfiles(perfil["username"])
        opcion: int = input_num_con_control(1,3)
        if opcion == 1:
            perfil_elegido: str = elegir_perfil(perfil)
            if perfil_elegido:
                if perfil["username"]: perfil.clear()
                perfil["username"] = perfil_elegido
        elif opcion == 2:
            nuevo_perfil()
        else:
            terminar: bool = True

######################### YOUTUBE: VALIDACION DE PERMISOS ##########################################
####################################################################################################

def validar_permisosYT(usuario: str) -> object:
    """ Corrobora que las credenciales para hacer solicitdudes a la API estén vigente.
    En caso de que no lo estén, solicita nuevas y genera un nuevo cliente. """
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

        return youtube          # Solo puede hacer 1 return
    else:                       
        return youtube

######################### OBTENCION DE DATOS #######################################################
####################################################################################################

def obtener_refresh_token_perfil(nombre: str) -> str:
    """Devuelve el refresh_token del nombre recibido, si el archivo de donde lo saca no esta entonces devuelve un str vacio."""
    datos_token: str = ""
    if os.path.isfile("datos_perfiles.json"):
        datos: dict = sacar_info_json("datos_perfiles.json")
        datos_token: str = datos[nombre]["spotify"]
    return datos_token


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


def ordenar_datos_playlist_SP(playlist) -> dict:            # Falta typing
    """Recibe un objeto y ..."""                               # Falta  documentacion
    datos_playlist: dict = {}
    datos_playlist["name"] = playlist.name
    datos_playlist["id"] = playlist.id
    datos_playlist["collaborative"] = playlist.collaborative
    datos_playlist["description"] = playlist.description
    return datos_playlist


def datos_playlists_SP(spotify: tk.Spotify, id_usuario: str) -> list:
    """
    Pre: Recibe un objeto spotify (ya con los datos de nuestro perfil elegido) y el id de Spotify del perfil actual.
    Post: Devuelve una lista con un monton de datos de las playlists que tiene el perfil actual.
    """
    datos: list = []
    datos_playlists: list = probando(spotify.playlists, [id_usuario, 50])
    if datos_playlists[0].items:  # Si hay playlists
        for playlist in datos_playlists[0].items:
            datos_playlist: dict = ordenar_datos_playlist_SP(playlist)
            datos.append(datos_playlist)
    elif datos_playlists: # Si no hay playlists
        datos.append("SIN PLAYLISTS")
    return datos

######################### AGREGARLE DATOS AL PERFIL ################################################
####################################################################################################

def probando(funcion_a_probar, datos_que_necesita: list = []) -> list:
    """
    Pre: Recibe una funcion junto con una lista de sus argumentos.
    Post: Devuelve una lista vacia si el usuario dejo de intentar que su funcion, bueno, funcionara.
          Caso contrario, devuelve una lista de un elemento con el dato buscado. 
    """
    terminar: bool = False
    dato: list = []
    while not terminar:
        try:
            if datos_que_necesita:
                dato_buscado = funcion_a_probar(*datos_que_necesita)
            else:
                dato_buscado = funcion_a_probar()
        except:
            print(vis.NO_INTERNET)
            print(" Necesitamos internet para acceder a los datos de su perfil.")
            intentar: str = input_con_control(["si", "no"], "Desea intentarlo de nuevo(si/no)?  ", 10, "Esta costando mucho.")
            if intentar == "no":
                terminar: bool = True
        else:
            dato.append(dato_buscado)
            terminar: bool = True
    return dato


def datos_necesarios_perfil(perfil: dict) -> None:
    """Le agrega datos sobre las plataformas al perfil recibido."""
    # Spotify:
    refresh_token: str = obtener_refresh_token_perfil(perfil["username"])
    if refresh_token:
        print("Consiguiendo datos de Spotify...")
        credenciales_SP: tuple = tuple(sacar_info_json("credenciales.json")["spotify"].values())
        datos_necesarios: list = [credenciales_SP[0], credenciales_SP[1], refresh_token] 
        token: list = probando(tk.refresh_user_token, datos_necesarios)
        if token:
            spotify: tk.Spotify = tk.Spotify(token[0])
            perfil["spotify"] = spotify
    if "spotify" in perfil:
        id_usuario: list = probando(spotify.current_user)
        if id_usuario:
            perfil["id_usuario_spotify"] = id_usuario[0].id 
        # Youtube:
        print("Consiguiendo datos de Youtube...")
        youtube = validar_permisosYT(perfil["username"])    # Falta typing
        perfil["youtube"] = youtube
        if "youtube" in perfil:
            request=youtube.channels().list(
                part= "id",
                mine= True
                )
            response: list = request.execute()["items"] # Devuelve una lista con la información del canal.
            id_YT: str = response[0]["id"]
            perfil["id_usuario_youtube"] = id_YT

####################################################################################################
####################################################################################################

def datos_agregados_correctamente(usuario_actual: dict) -> bool:
    """
    Pre: Recibe un diccionario con los datos asociados al usuario.
    Post: Devuelve False si encuentra que falta un dato necesario.
    """
    if usuario_actual["username"]:
        datos_buscar: list = [
            "spotify",
            "id_usuario_spotify",
            "youtube",
            "id_usuario_youtube",
            ]
        datos_necesarios_perfil(usuario_actual)
        estan_todos_los_datos: bool = all([dato in usuario_actual for dato in datos_buscar])
    else:
        estan_todos_los_datos: bool = False
    return estan_todos_los_datos
