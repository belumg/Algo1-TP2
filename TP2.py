import tekore as tk
from webbrowser import open as web_open
import TP2_VISUAL as vis

ID_CLIENTE: str = "ea4916f2e2d144a992b0f2d7bed6c25d"
URI_REDIRECCION: str = "http://localhost:8888/callback"
SCOPE = tk.scope.every
tk.client_id_var = "USUARIO_ID"


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

#### ----------------------------- AUTENTICACIÓN SPOTIFY ------------------------------------------
###################################################################################################

def datos_perfil_spotify(token) -> list:
    """
    Pre: Recibe un token de usuario (que aun no expiro) de Spotify.
    Post: Devuelve una lista [id_usuario, nombre_usuario]
    """
    datos_perfil :list = []
    spotify = tk.Spotify(token)
    usuario = spotify.current_user()
    datos_perfil.append(usuario.id)
    datos_perfil.append(usuario.display_name)
    return datos_perfil

def auntenticar_spotify(datos_importantes) -> None:
    try:
        token_usuario = tk.prompt_for_user_token(
            ID_CLIENTE,
            CLIENTE_SECRETO,
            URI_REDIRECCION,
            SCOPE
        )
    except KeyError:
        print("No ingresaste bien la URL")
        print("Intenta otra vez.")
    else:
        datos_importantes[1] = token_usuario

def guardar_nuevo_perfil(token, refresh_token) -> None:
    datos_usuario :list = datos_perfil_spotify(token)
    datos_guardar :tuple = (datos_usuario[0], None, None, refresh_token)
    tk.config_to_file("cuentas_spotify.txt", datos_guardar, datos_usuario[1])
    with open("nombres_spotify.txt", "a") as f:
        f.write(datos_usuario[1]+"\n")
    
def nuevo_perfil_spotify() -> None:
    credenciales :tk.Credentials = tk.Credentials(ID_CLIENTE, redirect_uri=URI_REDIRECCION)
    url, verificador = credenciales.pkce_user_authorisation(SCOPE)
    print(vis.INSTRUCCIONES)
    input("Presione Enter para que se abra Spotify: ")
    web_open(url)
    print()
    print("Aqui abajo debes ingresar la URL que copiaste:  ")
    url :str = input("--->  ").strip()
    codigo = tk.parse_code_from_url(url)
    token_usuario = credenciales.request_pkce_token(codigo, verificador)
    refresh_token = token_usuario.refresh_token
    guardar_nuevo_perfil(token_usuario, refresh_token)
    print(vis.DATOS_GUARDADOS)

def nuevo_perfil():
    vis.youtube_spotify()
    opcion :int = opciones([1,2])
    if opcion == 1:
        pass
    else:
        nuevo_perfil_spotify()

def manejo_perfiles():
    print(vis.MENU_PERFILES)
    opcion :int = opciones([1,2])
    if opcion == 1:
        pass
    else:
        nuevo_perfil()

#### ----------------------------- AUTENTICACIÓN YOUTUBE ------------------------------------------
###################################################################################################

### ----------------------------- ANALISIS DE PLAYLISTS -------------------------------------------
###################################################################################################

### Funciones reutilizables >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def print_playlists_nombres(lista_playlists:list) -> None:
    # !!! to-do !!!
    # mover a vis y modificar acorde
    for i in range(len(lista_playlists)):
        print(f'{i+1} - {lista_playlists[i]["name"]}')


def seleccionar_playlist(usuario_actual: dict, mi_playlist: dict) -> None:
    lista_spotify: list = list()
    lista_youtube: list = list()
    for playlist in usuario_actual['playlists_spotify']:
        lista_spotify.append(playlist['name'])
    for playlist in usuario_actual['playlists_youtube']:
        lista_youtube.append(playlist['snippet']['title'])

    vis.visual_nombres_playlists(lista_spotify, 'spotify')
    vis.visual_nombres_playlists(lista_youtube, 'youtube')

    print("Indique una plataforma")
    servidor = input(">>> ")
    while not servidor == "spotify" and not servidor == "youtube":
        servidor = input("Servidor inválido, vuelva a ingresar >>> ").lower()
    print("Seleccione una playlist ")
    seleccion = input(">>> ")
    while not seleccion.isnumeric and int(seleccion)<1:
        seleccion = input("Inválido. Vuelva a ingresar >>> ")
    seleccion = int(seleccion)

    if servidor == "spotify":
        if seleccion>len(lista_spotify):
            print("Número de playlist ingresado inválido.")
        else:
            mi_playlist['servidor'] = servidor
            mi_playlist['name'] = usuario_actual['playlists_spotify'][seleccion - 1]['name']
            mi_playlist['id'] = usuario_actual['playlists_spotify'][seleccion - 1]['id']

    elif servidor == "youtube":
        if seleccion>len(lista_youtube):
            print("Número de playlist ingresado inválido.")
        else:
            mi_playlist['servidor'] = servidor
            mi_playlist['name'] = usuario_actual['playlists_youtube'][seleccion - 1]['snippet']['title']
            mi_playlist['id'] = usuario_actual['playlists_youtube'][seleccion - 1]['id']


def normalizar_playlist_spotify(info_playlist:list, detalles:dict, playlist_id:str, playlist_nombre:str) -> None:
    detalles['id'] = playlist_id
    detalles['name'] = playlist_nombre
    detalles['tracks']= []
    detalles['owner'] = {
        'display_name': info_playlist[0]['owner']['display_name'],
        'id': info_playlist[0]['owner']['id'],
        'uri': info_playlist[0]['owner']['uri']
    }

    for i in (info_playlist[0]['tracks']['items']):

        detalles['tracks'].append(
                {'artists':  i['track']['artists'],
                'id': i['track']['id'],
                'name': i['track']['name'],
                'track_number': i['track']['track_number'],
                'uri': i['track']['uri']
                }
        )


def normalizar_playlist_youtube(info_playlist:list, detalles:dict, playlist_id:str, playlist_nombre:str) -> None:
    detalles['id'] = playlist_id
    detalles['name'] = playlist_nombre
    detalles['tracks'] = []
    detalles['owner'] = {
        'display_name': info_playlist[0]['snippet']['channelTitle'],
        'id': "unknown",
        'uri': "unknown"
    }

    for i in info_playlist:
        detalles['tracks'].append(
                {'artists': i['snippet']['videoOwnerChannelTitle'],
                 'id': i['id'],
                 'name': i['snippet']['title'],
                 'track_number': i['snippet']['position'],
                 'uri': 'unknown'
                 }
        )


def importar_playlist(token_spotify:str, token_youtube:str, playlist_id:str, playlist_nombre:str, servidor:str, detalles_playlist:dict) -> None:
    info_playlist:list=list()
    if servidor == "spotify":
        spotify = tk.Spotify(token_spotify)
        info_playlist.append(Spotify.playlist(spotify, playlist_id, fields=None, market=None, as_tracks=True))
        print(info_playlist)
        normalizar_playlist_spotify(info_playlist, detalles_playlist, playlist_id, playlist_nombre)
    elif servidor == "youtube":
        # !!! to-do!!!
        # ver cuando una playlist tiene +50 elementos
        youtube = token_youtube
        request = youtube.playlistItems().list(
            part="id, snippet, contentDetails",
            maxResults=50,
            playlistId=playlist_id
        )
        response = request.execute()
        for item in response['items']: #lista de dicts
            info_playlist.append(item)
        normalizar_playlist_youtube(info_playlist, detalles_playlist, playlist_id, playlist_nombre)


def exportar_dict_a_cvs(extension:str, usuario:str, mi_dict:dict, nombre:str) -> None:
    # Funciona para un solo dict, no nested dicts, y reescribe el archivo
    with open(f"{nombre}_{usuario}.{extension}", "w") as archivito:
        w = csv.DictWriter(archivito, mi_dict.keys())
        w.writeheader()
        w.writerow(mi_dict)



### Funciones propias del analisis de atributos >>>>>>>>>>>>>>>>>>>>>>>>

def analizar_track(track:dict, atributos_track:dict, token:str, atributos:list, servidor:str='spotify') -> None:
    if servidor == "spotify":
        spotify = tk.Spotify(token)
        # !!! to-do !!!
        # Ver si es necesario controlar esto:
        # if not track.episode and not track.is_local:
        print(f"Analizando track {track['name']}...\n")
        analisis = spotify.track_audio_features(track['id'])

        for atrib in atributos:
            atributos_track[atrib] = getattr(analisis, atrib)


def analisis_de_playlist(usuario_actual:dict) -> None:
    fecha = date.today()
    mi_playlist:dict=dict()
    atributos_playlist:dict={}
    atributos_track: dict = {}
    # info_playlist:dict= {}
    detalles_playlist: dict=dict()
    # atributos_playlist:dict:

    #     {
    #     fecha de analisis : object??
    #     id : str
    #     name: str
    #     atributo: int,
    #     atributo2: int,
    #     ...
    # }
    atributos: list = [
        'acousticness', 'danceability', 'energy', 'liveness', 'loudness',
        'valence', 'tempo', 'duration_ms', 'instrumentalness', 'speechiness'
    ]

    seleccionar_playlist(usuario_actual, mi_playlist)

    if mi_playlist['servidor'] == "spotify":
        importar_playlist(usuario_actual['token_spotify'], usuario_actual['token_youtube'], mi_playlist['id'],
                          mi_playlist['name'], mi_playlist['servidor'], detalles_playlist)
        for track in detalles_playlist['tracks']:
            analizar_track(track, atributos_track, usuario_actual['token_spotify'], atributos)
            for key,value in atributos_track.items():
                if atributos_playlist == {} and key not in atributos_playlist.keys():
                    atributos_playlist['fecha de analisis'] = fecha
                    atributos_playlist['id'] = detalles_playlist['id']
                    atributos_playlist['playlist name'] = detalles_playlist['name']
                    atributos_playlist[key] = value
                elif key not in atributos_playlist.keys():
                    atributos_playlist[key] = value
                else:
                    atributos_playlist[key] += value

        # !!! to-do !!!
        # mover a vis y modificar acorde
        for key,value in atributos_track.items():
            atributos_playlist[key] = value / len(detalles_playlist['tracks'])
            print(f"* {key} : {value}")
        exportar_dict_a_cvs('cvs', usuario_actual['username'], atributos_playlist, f"atributos_playlist_{mi_playlist['info']['id']}")
    else:
        print("No podemos realizar un analisis de atributos musicales para"
              " playlists en youtube.") #Youtube Music API when ??
        print("Le ofrecemos:"
              "[A] Sincronizar esta playlist con spotify y realizar el analisis de las canciones coincidentes.")
        print("[B] Dar un informe sobre los datos principales de esta playlist en el día de la fecha.")




### ------------------------ BÚSQUEDA DE CANCIONES ------------------------------------------------
###################################################################################################


def buscar_cancion(token_spotify: str, token_youtube: str, resultados: list) -> None:
    # Recibe resultados como list vacia para poder devolver las canciones de la búsqueda.
    # resultados:list = [
    #     {
    #         id: str,
    #         name: str,
    #         artista: list,
    #         album: str
    #     },
    #     ...
    # ]
    servidor = input("Ingrese el servidor en el que desea buscar: ").lower()
    while not servidor == "spotify" and not servidor == "youtube":
        servidor = input("Servidor inválido, vuelva a ingresar >>> ").lower()
    cancion = input("Ingrese el nombre de la canción a buscar >>> ")
    artista = input("Ingrese el artista >>> ")
    search = buscar_item(token_spotify, token_youtube, servidor, f"{cancion}, {artista}", 3, ('track', 'artist'))

    if servidor == "spotify":
        print("Buscando en spotify...")
        for x in search:  # tupla #object
            for item in x.items:
                item_n: dict = dict()
                item_n['id'] = item.id
                item_n['name'] = item.name
                item_n['artists'] = []
                item_n['album'] = item.album.name
                item_n['uri'] = item.uri
                for artist in item.album.artists:  # artists es lista en model
                    item_n['artists'].append(artist.name)
                    resultados.append(item_n)
    elif servidor == "youtube":
        print("Buscando en youtube...")
        print(search)
        for x in search['items']:  # dict
            item_n: dict = dict()
            item_n['id'] = x['id']['videoId']
            item_n['name'] = x['snippet']['title']
            item_n['artists'] = [x['snippet']['channelTitle']]
            item_n['album'] = "  "
            resultados.append(item_n)


def buscar_item(token_spotify:str, token_youtube:str, servidor:str, query:str, limit:int, types:tuple=('track',))-> None:
    if servidor == "spotify":
        spotify = tk.Spotify(token_spotify)
        # cambiando el tipo podemos buscar playlists, albums, artistas, etc
        search = spotify.search(query, types=types, market=None, include_external=None, limit=limit, offset=0)
    elif servidor == "youtube":
        youtube = token_youtube
        search = youtube.search().list(
            part="id, snippet",
            maxResults=limit,
            order="relevance",
            q=query
        )
        search = search.execute()

    return search



### ------------------------ ACCIONES POSTERIORES A BÚSQUEDA --------------------------------------
###################################################################################################

def agregar_cancion_a_youtube(playlist_id:str, cancion_id:str, token_youtube:str) -> None:
    youtube = token_youtube
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": cancion_id
                }
            }
        }
    )
    response = request.execute()


def agregar_a_playlist(usuario_actual:dict, cancion:dict) -> None:
    mi_playlist: dict = dict()

    seleccionar_playlist(usuario_actual, mi_playlist)

    if my_playlist['servidor'] == 'spotify':
        agregar_cancion_a_spotify(mi_playlist['info']['id'], cancion['uri'], usuario_actual['token_spotify'])
    elif my_playlist['servidor'] == 'youtube':
        agregar_cancion_a_youtube(mi_playlist['info']['id'], cancion['id'], usuario_actual['token_youtube'])


def agregar_cancion_a_spotify(playlist_id:str, uri_cancion:list, token:str) -> None:
    spotify = tk.Spotify(token)
    agregando = spotify.playlist_add(playlist_id, uri_cancion, position=None)

    if agregando.status_code == 200:
        print("Canción agregada correctamente")
    else:
        print("Ha habido un error al agregar la canción, intentelo nuevamente.")


def administracion_de_canciones(usuario_actual:dict) -> None:
    resultados: list = list()
    titulo: str = "Administrar canción"
    opciones: list = [
        "Visualizar", "Agregar a playlist"
    ]

    buscar_cancion(usuario_actual['token_spotify'], usuario_actual['token_youtube'], resultados)
    if len(resultados) > 0:
        print(f"""\n     Resultados de búsqueda""")
        for i in range(len(resultados)):
            mostrar_cancion(resultados[i], i)

        seleccion_cancion = input("Ingrese el codigo de la canción que buscaba >>> ")
        while not seleccion_cancion.isnumeric and int(seleccion_cancion)>3 and int(seleccion_cancion)<1:
            seleccion_cancion = input("Inválido. Vuelva a ingresa >>> ")
        seleccion_cancion = int(seleccion_cancion)

        menu_con_opciones_cortas(titulo, opciones)
        accion = input("     >>>")
        while not accion.isnumeric or int(accion)>2 or int(accion)<1:
            accion = input("Inválido. Vuelva a ingresa >>> ")

        if accion == "1":
            visualizar_cancion(resultados[seleccion_cancion], seleccion_cancion)
        else:
            agregar_a_playlist(usuario_actual, resultados[seleccion_cancion])

    else:
        print("No hemos obtenido ningún resultado de la búsqueda")


###------------------------- MANEJO DE LYRICS ------------------------------------------------------
###################################################################################################

def extraer_letra(token_genius, cancion: str = "0", artista: str = "0") -> str:
    genius = Genius(token_genius)
    # saca los headers
    genius.remove_section_headers = True
    # Exclude songs with these words in their title
    genius.excluded_terms = ["(Remix)", "(Live)", "(Cover)"]
    # Turn off status messages
    genius.verbose = False

    if cancion == "0" and artista == "0":
        es_cancion: bool = False
        while es_cancion == False:
            cancion = input("Nombre del cantante:")
            artista = input("Nombre de canción: ")
            song = genius.search_song(nombre_cancion, nombre_cantante)
            print(song)
            ser_o_no_ser: str = input("Es la canción que usted busca? (s/n)")
            if ser_o_no_ser in "sS":
                es_cancion = True
            else:
                es_cancion = False
    else:
        song = genius.search_song(cancion, artista)
        print("acá tambien")
    letra_song: str = str(song.lyrics)
    print("acá estuvo")
    return letra_song



def main() -> None:
  
    vis.inicio()
    manejo_perfiles()

    token_spotify: str = autenticar()
    token_youtube: str = " "

    # usuario_actual: dict= {
    #     'username': str,
    #     'token_spotify' : str,
    #     'token_youtube' : str,
    #     'playlists_youtube' : list,
    #     'playlists_spotify' : list
    # }

    ##### --------MENU PRINCIPAL DENTRO DEL PERFIL--------------------------
    print(vis.MENU)
    seleccion=input("      >>>    ")
    while not seleccion.isnumeric and int(seleccion)>3 and int(seleccion)<1:
        seleccion = input("Inválido. Vuelva a ingresar >>> ")
    seleccion=int(seleccion)

    if seleccion == 1:
        #Listar las playlist
        pass
    elif seleccion == 2:
        #Exportar analisis de playlist a CSV
        analisis_de_playlist(usuario_actual)
    elif seleccion == 3: 
        # Crear playlist
        pass
    elif seleccion == 4:
        #Buscar y administrar canción
        administracion_de_canciones(usuario_actual)
    elif seleccion == 5:
        #Sincronizar playlists
        pass
    elif seleccion == 6:
        #Generar wordcloud
        pass
    elif seleccion == 7: 
        #Cambiar de perfil
        pass

main()
