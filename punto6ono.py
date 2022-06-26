import tekore as tk
import requests
import csv

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "tp2_algo1.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)



################# COMPARACION DE BUSQUEDA CON LO QUE BUSCAMOS ################################
################### OBTENCION DE DATOS DE URI Y ID ##########################################3

def comparacion_con_search_spotify(search: tuple, nombre: str, artista: str, uris: list,  lista_no_encontrados: list)->None:
    # limpio el search con los cinco primeros.
    lista_encontrados: list = []
    for x in search:
        for item in x.items:
            for artist in item.album.artists:
                lista_encontrados.append([item.uri, item.name, artist.name])
    # verifico que sea esa cancion
    for i in range(len(lista_encontrados)):
        if lista_encontrados[i][1]==nombre:
            if lista_encontrados[i][2]==artista:
                uris.append(lista_encontrados[i][0])
                # como hay solo una cancion posible no tengo que preocuparme que agregue de mas
    for j in range(len(uris)):
        agrego: bool = False
        for k in range(len(lista_encontrados)):
            if uris[j] == lista_encontrados[k][0]:
                agrego = True
        if agrego == False:
            lista_no_encontrados.append([nombre, artista])



def comparacion_con_search_youtube(search: tuple, nombre: str, artista: str,
                               lista_no_encontrados: list) -> str:
    id_elejido: str = ""
    lista_encontrados=limpieza_yutub(search)
    for i in range(len(lista_encontrados)):
        if lista_encontrados[i][1]==nombre:
            if lista_encontrados[i][2]==artista:
                id.append(lista_encontrados[i][0])
    for j in range(len(id)):
        agrego: bool = False
        for k in range(len(lista_encontrados)):
            if id[j] == lista_encontrados[k][0]:
                agrego = True
        if agrego == False:
            lista_no_encontrados.append([nombre, artista])
            id_elejido = "no habemus nada"

        else:
            id_elejido= id[0]
            # elijo el primero porque hay millones de videos posibles para una sola cancion
    return id_elejido

################################################################################

#--------------------------------------------------------------------------


######################## CREAR LISTAS ##############################

def crear_playlist_spotify(user_id: str, token: str)->str:
    spotify = tk.Spotify(token)
    nombre: str = input("indique el nombre para la playlist en spotify")
    publica: str = input("indique si desea que sea publica (s/n)")
    if publica in "sS":
        public: bool = True
    descripcion: str = input("indique descripción: ")
    spotify.playlist_create(user_id, nombre, public, descripcion)
    return nombre


def crear_playlist_youtube(token_yutub:str )->str:
    youtube = token_yutub
    nombre: str = input("Indicame el nombre bebe: ")
    descripcion: str = input("La descripcion please")
    privaciti: str = input("Privado (p) o no privado (n) esa es la cuestion")
    i:int = 0
    while privaciti!="p" and privaciti!="n":
        i = i + 1
        if i==2:
            print("Mire que no tenemos todo el dia")
        privaciti = input("Por favor escriba correctamente")
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
    return nombre

######################################################################
#-------------------------------------------------------------

################### IDS DE PLAYLIST UNA VEZ CREADA ####################

def dame_id_playlist(token, user_id, nombre, servicio)->str:
    if servicio=="spotify":
        spotify = tk.Spotify(token)
        playlist = spotify.playlists(user_id, limit=100)
        for i in range(len(playlist.items)):
            if playlist.items[i].name == nombre:
                playlist_id: str = playlist.items[i].id

    elif servicio=="youtube":
        youtube=token
        request = youtube.playlists().list(
            part="id, snippet",
            mine=True
        )
        response = request.execute()
        for i in response['items']:
            if response['items'][i]['snippet']['title'] == nombre:
                playlisy_id: str = response['items'][i]['id']
    return playlist_id


####################################################################
#-----------------------------------------------------------------


############## CANCIONES YA EN LA LISTA #############################

def lista_canciones(info_playlist: dict, lista_cancion: list)->None:
        for i in  info_playlist['tracks']['items']:
            cancion: str = info_playlist['tracks']['items'][i]['name']
            artista: str = info_playlist['tracks']['items'][i]['artists']
            lista_cancion.append([cancion,artista])



def comparacion(lista_yutub: list, lista_spotifai: list, servicio_base: str)->list:
        # comparar ambas listas para no agregar repetidos
    lista_a_agregar: list = []
    if servicio_base == "spotify":
        for i in range(len(lista_spotifai)):
            esta: bool = False
            for j in range(len(lista_yutub)):
                if lista_spotifai[i]==lista_yutub[j]:
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


###############################################################


def limpieza_yutub(search: dict)->list:
    lista_encontrados: list = []
    for i in search['items']:
        titulo: str = (search['items'][i]['snippet']['title'])
        id: str = (search['items'][i]['id']['videoId'])
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



############### PROGRAMA EN ESPECIAL ###############################

def spotify_vs_youtube(usuario_actual: dict, token_spotifai: str, token_yutub: str, user_id_spotifai: str, user_id_yutub: str):
    spotify = tk.Spotify(token_spotifai)
    opcion: str = input("Indicar si es de spotify a youtube (1) o"
                        " de youtube a spotify (2)\n >>>")
    # donde se va a guardar la informacion de la lista de spotify
    playlist_spotifai: dict = {}
    detalles_spotifai: dict = {}
    # aca se va a guardar la informacion de la lista de youtube
    playlist_yutub: dict = {}
    detalles_yutub: dict = {}

    # donde se guardaran las uris para pasarlas
    uris: list = []

    while opcion != "1" and opcion != "2":
        opcion = input("Solo hay dos opciones")
    opcion: int = int(opcion)

########## DE SPOTIFAI AL YUTUB ###########################


    if opcion == 1:
        # spotify a youtube
        lista_spotifai: list = []
        seleccionar_playlist(usuario_actual, playlist_spotifai)
        # recibo la informacion de la lista elegida
        normalizar_playlist(playlist_spotifai, detalles_spotifai)
        lista_canciones(detalles_spotifai, lista_spotifai)
        # ahora tengo que saber si quiere crear una nueva o no
        opcion2: str = input("Quiere crear nueva playlist (1) o quiere realizarlo en una ya creada (2)")
        while opcion2 != "1" and opcion2 != "2":
            opcion2 = input("solo hay dos opciones.")
        opcion2: int = int(opcion2)
        if opcion2 == 1:
            # crear lista de youtube
            nombre = crear_playlist_youtube(token_yutub)
            playlist_id = dame_id_playlist(token_yutub,user_id_yutub, nombre, "youtube")
            lista_yutub: list = []
        else:
            # uso una ya conocida
            lista_yutub: list = []
            seleccionar_playlist(usuario_actual, playlist_yutub)
            # recibo la informacion de la lista elegida
            normalizar_playlist(playlist_yutub, detalles_yutub)
            playlist_id: str = detalles_yutub['id']
            lista_canciones(detalles_yutub, lista_yutub)
        lista_agregar: list = comparacion(lista_yutub, lista_spotifai, "spotify")
        lista_no_agregado: list = []
        # uris de las canciones
        for i in lista_agregar:
            search = buscar_item(token_spotifai, token_yutub, "spotify",
                                 f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 5, ('track', 'artist'))
            id: str = comparacion_con_search_youtube(search, lista_agregar[i][0], lista_agregar[i][1],
                                           lista_no_agregado)
            if id!="no habemus nada":
                agregar_cancion_a_youtube(playlist_id, id, token_yutub)
            # se agrega las canciones encontradas


############### DE YOUTUBE A SPOTIFY ###########################
# A ESTE PUNTO LA PROGRAMADORA SE ESTA PREGUNTANDO SI ES BUENA IDEA SEGUIR VIVIENDO

    else:
        lista_yutub : list = []
        # youtube a spotify
        seleccionar_playlist(usuario_actual, playlist_yutub)
        # recibo la informacion de la lista elegida
        normalizar_playlist(playlist_yutub, detalles_yutub)
        lista_canciones(detalles_yutub, lista_yutub)
        opcion2: str = input("Quiere crear nueva playlist (1) o quiere realizarlo en una ya creada (2)")
        while opcion2 != "1" and opcion2 != "2":
            opcion2 = input("solo hay dos opciones.")
        opcion2: int = int(opcion2)
        if opcion2 == 1:
            # creo la playlist de spotify
            lista_spotifai: list = []
            nombre: str = crear_playlist_spotify(user_id_spotifai, token_spotifai)
            # como recibo la informacion de la playlist que elegí, necesito id
            # hay que hacerlo con TRY
            playlist_id = dame_id_playlist(token_spotifai, user_id_spotifai, nombre,'spotify')
            # normalizar??
            playlist_spotifai = spotify.playlist(playlist_id)
            normalizar_playlist(playlist_spotifai, detalles_spotifai)
            lista_canciones(detalles_spotifai, lista_spotifai)

        elif opcion2 == 2:
            # uso una de las de ahí
            lista_spotifai: list = []
            seleccionar_playlist(usuario_actual, playlist_spotifai)
            # recibo la informacion de la lista elegida
            normalizar_playlist(playlist_spotifai, detalles_spotifai)
            lista_canciones(detalles_spotifai, lista_spotifai)
        lista_agregar: list = comparacion(lista_yutub, lista_spotifai, "youtube")
        uris: list = []
        lista_no_agregado: list = []
        # uris de las canciones
        for i in lista_agregar:
            search = buscar_item(token_spotifai, token_yutub, "spotify",
                                     f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 5, ('track', 'artist'))
            comparacion_con_search_spotify(search, lista_agregar[i][0], lista_agregar[i][1], uris,
                                               lista_no_agregado)
            # se agrega las canciones encontradas
        spotify.playlist_add(playlist_id, uris, position=None)
        # se imprime las que no al final


    # paso la información al archivo csv
    #exportar_dict_a_archivo('csv', user_id, dict_no_se_pudo, detalles['name'])


################### PARTE DE DANI ########################

def normalizar_playlist(info_playlist:dict, detalles:dict) -> None:
    # Tecnicamente se podria lograr manejando los fields en spotify.playlists
    # pero queria una función que pudiera aplicar a youtube también
    # !!! REVEER CUANDO ESTE LO DE YOUTUBE, ¿VALE LA PENA?
    detalles['collaborative'] = info_playlist['collaborative']
    detalles['description'] = info_playlist['description']
    detalles['external_urls'] = info_playlist['external_urls']
    detalles['id'] = info_playlist['id']
    detalles['name'] = info_playlist['name']
    detalles['owner'] = {
        'display_name': info_playlist['owner']['display_name'],
        'id': info_playlist['owner']['id'],
        'uri': info_playlist['owner']['uri']
    }
    detalles['tracks']= {
        'items': []
    }

    for i in info_playlist['tracks']['items']:
        detalles['tracks']['items'].append({
            'track':
                {'artists':  i['track']['artists'],
                'id': i['track']['id'],
                'name': i['track']['name'],
                'track_number': i['track']['track_number'],
                'uri': i['track']['uri']
                }
        })


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


def buscar_item(token_spotify:str, token_youtube:str, servidor:str, query:str, limit:int, types:tuple=('track',)):
    if servidor == "spotify":
        spotify = tk.Spotify(token_spotify)
        # cambiando el tipo podemos buscar playlists, albums, artistas, etc
        search = spotify.search(query, types=types, market=None, include_external=None, limit=limit, offset=0)
    elif servidor == "youtube":
        # youtube = googleapiclient.discovery.build(
        #     "youtube", "v3", credentials=token_youtube)
        youtube = token_youtube
        search = youtube.search().list(
            part="id, snippet",
            maxResults=limit,
            order="relevance",
            q=query,
        )
        search = search.execute()

    return search


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


def normalizar_playlist_spotify(info_playlist: list, detalles: dict, playlist_id: str, playlist_nombre: str) -> None:
    detalles['id'] = playlist_id
    detalles['name'] = playlist_nombre
    detalles['tracks'] = []
    detalles['owner'] = {
        'display_name': info_playlist[0]['owner']['display_name'],
        'id': info_playlist[0]['owner']['id'],
        'uri': info_playlist[0]['owner']['uri']
    }

    for i in (info_playlist[0]['tracks']['items']):
        detalles['tracks'].append(
            {'artists': i['track']['artists'],
             'id': i['track']['id'],
             'name': i['track']['name'],
             'track_number': i['track']['track_number'],
             'uri': i['track']['uri']
             }
        )


def normalizar_playlist_youtube(info_playlist: list, detalles: dict, playlist_id: str, playlist_nombre: str) -> None:
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


def importar_playlist(token_spotify: str, token_youtube: str, playlist_id: str, playlist_nombre: str, servidor: str,
                      detalles_playlist: dict) -> None:
    info_playlist: list = list()
    if servidor == "spotify":
        spotify = tk.Spotify(token_spotify)
        info_playlist.append(spotify.playlist(playlist_id, fields=None, market=None, as_tracks=True))
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
        for item in response['items']:  # lista de dicts
            info_playlist.append(item)
        normalizar_playlist_youtube(info_playlist, detalles_playlist, playlist_id, playlist_nombre)

