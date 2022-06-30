import os
import json
from csv import DictWriter
import TP2_VISUAL as vis
import TP2_PERFILES as perf

####################################################################################################
####################################################################################################

def input_num_con_control(min:int, max:int) -> int:
    seleccion = input("      >>>    ")
    while not seleccion.isnumeric() or int(seleccion) > max or int(seleccion) < min:
        seleccion = input("Inválido. Vuelva a ingresar >>> ")
    return int(seleccion)

######################### SINCRONIZAR PLAYLISTS ####################################################
####################################################################################################

def exportar_dict_a_cvs(extension:str, usuario:str, mi_dict:dict, nombre:str) -> None:
    # Funciona para un solo dict, no nested dicts, y reescribe el archivo
    with open(f"{nombre}_{usuario}.{extension}", "w") as archivito:
        w = DictWriter(archivito, mi_dict.keys())
        w.writeheader()
        w.writerow(mi_dict)


def comparacion_con_search_spotify(search: tuple, nombre: str, artista: str, uris: list,
                                   lista_no_encontrados: list) -> None:
    # limpio el search con los cinco primeros.
    lista_encontrados: list = []
    for x in search:
        for item in x.items:
            for artist in item.album.artists:
                lista_encontrados.append([item.uri, item.name, artist.name])
    # verifico que sea esa cancion
    for i in range(len(lista_encontrados)):
        if lista_encontrados[i][1] == nombre:
            if lista_encontrados[i][2] == artista:
                uris.append(lista_encontrados[i][0])
                # como hay solo una cancion posible no tengo que preocuparme que agregue de mas
    for j in range(len(uris)):
        agrego: bool = False
        for k in range(len(lista_encontrados)):
            if uris[j] == lista_encontrados[k][0]:
                agrego = True
        if agrego == False:
            lista_no_encontrados.append([nombre, artista])


def sincronizacion_youtube_a_spotify(usuario_actual: dict, playlist_spotifai: dict, detalles_spotifai: dict,
                                     token_yutub: object, user_id_spotifai: str,  playlist_yutub : dict,
                                     detalles_yutub: dict, spotify: object) -> dict:
    # A ESTE PUNTO LA PROGRAMADORA SE ESTA PREGUNTANDO SI ES BUENA IDEA SEGUIR VIVIENDO
    lista_yutub: list = []
    # youtube a spotify
    print_playlists_de_user(usuario_actual, "youtube")
    seleccionar_playlist(usuario_actual, playlist_yutub, "youtube")
    # recibo la informacion de la lista elegida
    importar_playlist(spotify, token_yutub, playlist_yutub['id'], playlist_yutub['name'],
                      "youtube", detalles_yutub)
    lista_canciones(detalles_yutub, lista_yutub, "youtube")
    opcion2: str = input("Quiere crear nueva playlist (1) o quiere realizarlo en una ya creada (2)")
    while opcion2 != "1" and opcion2 != "2":
        opcion2 = input("solo hay dos opciones.")
    opcion2: int = int(opcion2)
    if opcion2 == 1:
        # creo la playlist de spotify
        lista_spotifai: list = []
        nombre: str = crear_playlist_spotify(user_id_spotifai, spotify)
        # como recibo la informacion de la playlist que elegí, necesito id
        # hay que hacerlo con TRY
        playlist_id = dame_id_playlist(spotify, token_yutub, user_id_spotifai, nombre, 'spotify')
        # normalizar??
        playlist_spotifai = spotify.playlist(playlist_id)
        importar_playlist(spotify, token_yutub, playlist_yutub['id'], playlist_yutub['name'],
                          "spotify", detalles_spotifai)
        lista_canciones(detalles_spotifai, lista_spotifai, "spotify")

    elif opcion2 == 2:
        # uso una de las de ahí
        lista_spotifai: list = []
        print_playlists_de_user(usuario_actual, "spotify")
        seleccionar_playlist(usuario_actual, playlist_spotifai, "spotify")
        # recibo la informacion de la lista elegida
        importar_playlist(spotify, token_yutub, playlist_yutub['id'], playlist_yutub['name'],
                          "spotify", detalles_spotifai)
        lista_canciones(detalles_spotifai, lista_spotifai, "spotify")
    lista_agregar: list = comparacion(lista_yutub, lista_spotifai, "youtube")
    print(lista_agregar)
    uris: list = []
    lista_no_agregado: list = []
    # uris de las canciones
    for i in range(len(lista_agregar)):
        search = buscar_item(spotify, token_yutub, "spotify",
                             f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 5, ('track', 'artist'))
        comparacion_con_search_spotify(search, lista_agregar[i][0], lista_agregar[i][1], uris,
                                       lista_no_agregado)
        # se agrega las canciones encontradas
    spotify.playlist_add(playlist_id, uris, position=None)
    no_se_pudo: dict = {}
    no_se_pudo['no se pudo'] = lista_no_agregado
    return no_se_pudo


def agregar_cancion_a_youtube(playlist_id: str, cancion_id: str, youtube: object) -> None:
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
    print(response)


def limpieza_yutub(search: dict)->list:
    lista_encontrados: list = []
    for i in search['items']:
        titulo: str = i['snippet']['title']
        id: str = i['id']['videoId']
        # titulo real
        # forma del kpop
        if "&#39;" in titulo:
            star: int = titulo.find('&')
            comienzo: int = titulo.find(';')
            cantante = titulo[0:star]
            cancion: str = titulo[comienzo + 1:len(titulo)]
            fin: int = cancion.find('&#39; ')
            cancion = cancion[0:fin]

        # forma del pop
        elif "-" in titulo:
            comienzo: int = titulo.find('-')
            cantante: str = titulo[0:comienzo - 1]
            cancion = titulo[comienzo + 2:len(titulo)]
            if '(' in cancion:
                fin: int = cancion.find('(')
                cancion = cancion[0:fin]
            if '[' in cancion:
                fin: int = cancion.find('[')
                cancion = cancion[0:fin]
        else:
            cancion: str = titulo
            cantante: str = search['items'][0]['channelTitle']
        while '&#39;' in cancion:
            principito: int = cancion.find('&')
            final: int = cancion.find(';')
            apostrofe: str = "'"
            cancion_corregida: str = cancion[0:principito] + apostrofe + cancion[final + 1:len(cancion)]
            cancion = cancion_corregida
        lista_encontrados.append([id, cancion, cantante])
        return lista_encontrados


def comparacion_con_search_youtube(search: tuple, nombre: str, artista: str,
                                   lista_no_encontrados: list, spotify: object,
                                   token_youtube: object)-> str:
    id_elegido: str = ""
    id: list = []
    lista_encontrados = limpieza_yutub(search)
    for i in range(len(lista_encontrados)):
        if lista_encontrados[i][1] == nombre:
            if lista_encontrados[i][2] == artista:
                id.append(lista_encontrados[i][0])
    for j in range(len(id)):
        agrego: bool = False
        for k in range(len(lista_encontrados)):
            if id[j] == lista_encontrados[k][0]:
                agrego = True
        if agrego == False:
            lista_no_encontrados.append([nombre, artista])
            id_elegido = "no habemus nada"

        else:
            id_elegido = id[0]
            # elijo el primero porque hay millones de videos posibles para una sola cancion
    return id_elegido


def buscar_item(spotify:object, token_youtube:object, servidor:str, query:str, limit:int, types:tuple=('track',))-> tuple:
    if servidor == "spotify":
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


def comparacion(lista_yutub: list, lista_spotifai: list, servicio_base: str)->list:
        # comparar ambas listas para no agregar repetidos
    lista_a_agregar: list = []
    if servicio_base == "spotify":
        for i in range(len(lista_spotifai)):
            esta: bool = False
            for j in range(len(lista_yutub)):
                if lista_spotifai[i] == lista_yutub[j]:
                    esta = True
            if esta == False:
                lista_a_agregar.append(lista_spotifai[i])
    if servicio_base == "youtube":
        for i in range(len(lista_yutub)):
            esta: bool = False
            for j in range(len(lista_spotifai)):
                if lista_yutub[i] == lista_spotifai[j]:
                    esta = True
            if esta == False:
                lista_a_agregar.append(lista_yutub[i])
    print(lista_a_agregar)
    return lista_a_agregar


def dame_id_playlist(spotify: object, token_youtube: object, user_id: str, nombre: str, servicio: str)->str:
    if servicio == "spotify":
        playlist = spotify.playlists(user_id, limit=50)
        for i in range(len(playlist.items)):
            if playlist.items[i].name == nombre:
                playlist_id: str = playlist.items[i].id

    elif servicio == "youtube":
        youtube = token_youtube
        request = youtube.playlists().list(
            part = "id, snippet",
            mine = True
        )
        response = request.execute()
        print(response)
        for i in response['items']:
            if i['snippet']['title'] == nombre:   # i["snippet"]["title"] = "Copiado de Spotify"
                playlist_id: str = i['id']        # nombre = batmancito 
    return playlist_id


def lista_canciones(info_playlist: dict, lista_cancion: list, servidor: str) -> None:
    artistas:list = []
    if servidor == "spotify":
        for i in range(len(info_playlist['tracks'])):
            artistas: list = []
            cancion: str = info_playlist['tracks'][i]['name']
            for j in range(len(info_playlist['tracks'][i]['artists'])):
                artistas.append(info_playlist['tracks'][i]['artists'][j]['name'])
            lista_cancion.append([cancion, ','.join(artistas)])
    if servidor == "youtube":
        for i in range(len(info_playlist['tracks'])):
            cancion: str = info_playlist['tracks'][i]['name']
            artistas = (info_playlist['tracks'][i]['artists'])
            # for j in range(len(info_playlist['tracks'][i]['artists'])):
            #     artistas.append(info_playlist['tracks'][i]['artists'][j])
            # print(artistas)
            lista_cancion.append([cancion, artistas])


def normalizar_playlist_spotify(info_playlist:list, detalles:dict,
                                playlist_id:str, playlist_nombre:str) -> None:
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


def importar_playlist(spotify:object, token_youtube:object, playlist_id:str, playlist_nombre:str,
                      servidor:str, detalles_playlist:dict) -> None:

    info_playlist: list = list()
    if servidor == "spotify":
        info_playlist.append(spotify.playlist(playlist_id, as_tracks=True))
        #info_playlist.append(Spotify.playlist(spotify, playlist_id, fields=None, market=None, as_tracks=True))
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


def comprobar_permisos(usuario_actual:dict, servidor:str, seleccion:int) -> bool:  # PROBLEM: FALTA TYPING
    permitido: bool = False
    if servidor == "spotify":
        id: str = usuario_actual["playlists_spotify"][seleccion - 1]["id"]
        if usuario_actual["playlists_spotify"][seleccion - 1]["collaborative"]:
            permitido = True
        else:
            spotify = usuario_actual["spotify"]
            owner_playlist = spotify.playlist(id).owner
            if owner_playlist.id == usuario_actual['id_usuario_spotify']:
                permitido: bool = True
    return permitido


def seleccionar_playlist(usuario_actual:dict, mi_playlist:dict, servidor:str, permisos:bool = False) -> None:
    permitido : bool = False
    print("Seleccione una playlist ")
    seleccion: int = input_num_con_control(1, len(usuario_actual[f'playlists_{servidor}']))  # PROBLEM: REVISAR (LE AGREGO +1?)
    permitido = comprobar_permisos(usuario_actual, servidor, seleccion)   # PROBLEM: SI ENTRA CON YOUTUBE SIEMPRE DEVUELVE UN FALSE
    while servidor == "spotify" and permisos and not permitido:   # PERMISOS ES FALSE
        print("No puede modificar esa playlist. Elija una suya o que sea colaborativa.")
        seleccion = input_num_con_control(1, len(usuario_actual[f'playlists_{servidor}']+1))
        permitido = comprobar_permisos(usuario_actual, servidor, seleccion)
    mi_playlist['servidor'] = servidor              # Guarda en un diccionario de afuera
    mi_playlist['name'] = usuario_actual[f"playlists_{servidor}"][seleccion - 1]['name']
    mi_playlist['id'] = usuario_actual[f"playlists_{servidor}"][seleccion - 1]['id']


def sincronizacion_spotify_a_youtube(usuario_actual: dict, playlist_spotify: dict, detalles_spotify: dict,
                                     youtube: object, user_id_yutub: str, playlist_yutub : dict,
                                     detalles_yutub: dict, spotify: object) -> dict:
    # SPOTIFY --> YOUTUBE
    lista_spotify: list = []
    print_playlists_de_user(usuario_actual, "spotify")
    if hay_playlists(usuario_actual, "spotify"):
        seleccionar_playlist(usuario_actual, playlist_spotify, "spotify")
        print(playlist_spotify)
        # recibo la informacion de la lista elegida
        importar_playlist(spotify, youtube, playlist_spotify['id'],
                        playlist_spotify['name'],
                        "spotify", detalles_spotify)
        lista_canciones(detalles_spotify, lista_spotify, "spotify")
        # ahora tengo que saber si quiere crear una nueva o no
        opcion2: str = input("Quiere crear nueva playlist (1) o quiere realizarlo en una ya creada (2): ")  # CAPAZ LE PONGA UNA CONSTANTE
        while opcion2 != "1" and opcion2 != "2":
            opcion2 = input("Solo hay dos opciones. Intenta de nuevo: ")
        opcion2: int = int(opcion2)
        if opcion2 == 1:
            # crear lista de youtube
            nombre, playlist_id = crear_playlist_youtube(youtube)
            #playlist_id = dame_id_playlist(spotify, youtube, user_id_yutub, nombre, "youtube")
            lista_yutub: list = []
        else:
            # uso una ya conocida
            lista_yutub: list = []
            print_playlists_de_user(usuario_actual, "youtube")
            seleccionar_playlist(usuario_actual, playlist_yutub, "youtube")
            # recibo la informacion de la lista elegida
            importar_playlist(spotify, youtube, playlist_yutub['id'],playlist_yutub['name'],
                            "youtube", detalles_yutub)
            playlist_id: str = detalles_yutub['id']
            lista_canciones(detalles_yutub, lista_yutub, "youtube")
        lista_agregar = comparacion(lista_yutub, lista_spotify, "spotify")
        print(lista_agregar)
        lista_no_agregado: list = []
        # uris de las canciones
        for i in range(len(lista_agregar)):
            search = buscar_item(spotify, youtube, "youtube",
                                f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 5, ('track', 'artist'))
            id: str = comparacion_con_search_youtube(search, lista_agregar[i][0], lista_agregar[i][1],
                                        lista_no_agregado,spotify, youtube)
            print(id)
            if id != "no habemus nada":
                agregar_cancion_a_youtube(playlist_id, id, youtube)
        no_se_pudo: dict = {}
        no_se_pudo['no se pudo'] = lista_no_agregado
        return no_se_pudo
    else:
        print(" Necesitamos si o si que tenga una playlist para hacer una sincronizacion.")


def spotify_vs_youtube(usuario_actual: dict, spotify: object, token_youtube: object, user_id_spotify: str,
                       user_id_yutub: str):
    print(vis.DE_QUE_LADO)
    opcion = input_num_con_control(1,3)
    # donde se va a guardar la informacion de la lista de spotify
    playlist_spotify: dict = {}
    detalles_spotify: dict = {}
    # aca se va a guardar la informacion de la lista de youtube
    playlist_yutub: dict = {}
    detalles_yutub: dict = {}
    if opcion == 1:
        no_se_pudo: dict = sincronizacion_spotify_a_youtube(usuario_actual, playlist_spotify, detalles_spotify,
                                     token_youtube, user_id_yutub, playlist_yutub, detalles_yutub,
                                    spotify)
    elif opcion == 2:
        no_se_pudo: dict = sincronizacion_youtube_a_spotify(usuario_actual, playlist_spotify, detalles_spotify,
                                       token_youtube, user_id_spotify,  playlist_yutub,
                                         detalles_yutub, spotify)
        exportar_dict_a_cvs("csv", usuario_actual['name'], no_se_pudo, "no se pudo")

######################### CREAR PLAYLISTS ##########################################################
####################################################################################################

def crear_playlist_spotify(user_id: str, spotify: object) -> str:
    nombre: str = input("Indique el nombre para la playlist en Spotify: ")
    publica: str = input("Indique si desea que sea publica (s/n): ")   # PROBLEM: REVISAR ESTO
    if publica in "sS":
        public: bool = True
    else:
        public: bool = False
    descripcion: str = input("Indique descripción: ")
    spotify.playlist_create(user_id, nombre, public, descripcion)
    return nombre                                                        # PROBLEM: POR QUE DEVUELVE ESTO?


def crear_playlist_youtube(token_youtube: object) -> tuple:
    youtube = token_youtube
    nombre: str = input("Indicame el nombre bebe: ")                       # PROBLEM: TREMENDO
    descripcion: str = input("La descripcion please: ")
    privaciti: str = input("Privado (p) o no privado (n) esa es la cuestion: ")         
    i: int = 0
    while privaciti != "p" and privaciti != "n":                            # PROBLEM: PODEMOS CREAR UNA FUNCION SOLO PARA ESTO
        i = i + 1
        if i == 2:
            print("Mire que no tenemos todo el dia.")
        privaciti = input("Por favor escriba correctamente: ")
    if privaciti in "pP":
        privaciti = 'private'
    else:
        privaciti = 'public'
    playlists_insert_response = youtube.playlists().insert(                  
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=nombre,
                description=descripcion
            ),
            status=dict(
                privacyStatus=privaciti
            )
        )
    ).execute()

    return nombre, playlists_insert_response["id"]


def crear_playlist(user_id: str, spotify: object, token_youtube: object)->None:
    vis.youtube_spotify()
    opcion: str = input(">>> ")
    while opcion!="1" and opcion!="2" and opcion!="3":                              # PROBLEM: REVISAR ESTO
        opcion = input("Solo le estoy pidiendo que ingrese numeros no me haga enojar: ")
    opcion: int = int(opcion)
    if opcion == 1:
        crear_playlist_spotify(user_id, spotify)
    else:
        crear_playlist_youtube(token_youtube)

######################### IMPRIMIR PLAYLISTS #######################################################
####################################################################################################

def hay_playlists(usuario_actual: dict, plataforma: str) -> bool:
    return not len(usuario_actual[f'playlists_{plataforma}']) == 0

def print_playlists_de_user(usuario_actual:dict, plataforma:str) -> None:
    lista_nombres: list = list()
    if not hay_playlists(usuario_actual, plataforma):
        print(vis.NO_PLAYLIST)
    else:
        for playlist in usuario_actual[f'playlists_{plataforma}']:
            lista_nombres.append(playlist['name'])
    vis.visual_lista_elementos(lista_nombres, f"Playlists de {plataforma}", True)


def playlist_segun_servidor(usuario_actual: dict) -> str:
    vis.youtube_spotify(ambas=True)
    seleccion = input_num_con_control(1,3)   # PROBLEM: UNA OPCION VOLVER AL MENU
    if seleccion == 1:
        print_playlists_de_user(usuario_actual, "spotify")
        servidor: str = "spotify"
    elif seleccion == 2:
        print_playlists_de_user(usuario_actual, "youtube")
        servidor: str = "youtube"
    elif seleccion == 3:
        print_playlists_de_user(usuario_actual, "spotify")
        print_playlists_de_user(usuario_actual, "youtube")
        servidor: str = "unknown"
    return servidor

######################### REVISION DE CREDENCIALES #################################################
####################################################################################################

def estan_archivos():
    """Devuelve True si encuentra los 2 archivos donde estan las credenciales que necesitamos, caso contrario devuelve False."""
    if not os.path.isfile("credenciales_YT.json"):
        vis.falta_archivo("YT")
        return False
    if not os.path.isfile("credenciales_SP.json"):
        vis.falta_archivo("SP")
        return False
    return True


def conseguir_credenciales_spotify() -> tuple:
    with open("credenciales_SP.json") as f:
        datos = json.load(f)
    return tuple(datos.values())

####################################################################################################
####################################################################################################

def main() -> None:
    if estan_archivos():
        vis.inicio()
        credenciales_spotify: tuple = conseguir_credenciales_spotify()
        usuario_actual: dict = {"username": ""}
        perf.manejo_perfiles(usuario_actual, credenciales_spotify)
        terminar: bool = True
        if perf.datos_agregados_correctamente(usuario_actual, credenciales_spotify):
            terminar: bool = False
        print(usuario_actual)
        while not terminar:
            print(vis.MENU)
            seleccion: int = input_num_con_control(0, 7)
            if seleccion == 1:
                #Listar las playlist
                playlist_segun_servidor(usuario_actual)

            #elif seleccion == 2:
                #Exportar analisis de playlist a CSV            
                #analisis_de_playlist(usuario_actual)

            elif seleccion == 3:
                # Crear playlist
                crear_playlist(usuario_actual['id_usuario_spotify'], usuario_actual['spotify'],
                            usuario_actual['youtube'])

            #elif seleccion == 4:
                #Buscar y administrar canción
                #administracion_de_canciones(usuario_actual)
            elif seleccion == 5:
                #Sincronizar playlists
                spotify_vs_youtube(usuario_actual, usuario_actual['spotify'], usuario_actual['youtube'],
                                usuario_actual['id_usuario_spotify'], usuario_actual['id_usuario_youtube'])
            #elif seleccion == 6:
                #Generar wordcloud
                #wordcloud(usuario_actual, usuario_actual['spotify'], usuario_actual['youtube'])

            elif seleccion == 7:
                #Cambiar de perfil
                perf.manejo_perfiles(usuario_actual, credenciales_spotify)
                if not perf.datos_agregados_correctamente(usuario_actual, credenciales_spotify):
                    terminar: bool = True
            else:
                terminar: bool = True

main()
