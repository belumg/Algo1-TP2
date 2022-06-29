import matplotlib.pyplot as plt
import cv2 as cv
import tekore as tk
from webbrowser import open as web_open
import TP2_VISUAL as vis
from tekore import Spotify
import requests
from lyricsgenius import Genius
import time
import csv
import os
from datetime import date
import json
import google_auth_oauthlib.flow
import google.auth.transport.requests
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


#### ----------------------------- CREDENTIALS SPOTIFY  -------------------------------------------
###################################################################################################

ID_CLIENTE: str = "176365611325455e8059fbd545371d89"
CLIENTE_SECRETO: str = "ed35a90b681042f4bbad9f284383c88a"
URI_REDIRECCION: str = "http://localhost:8888/callback"
SCOPE: tk.Scope = tk.scope.every

###################################################################################################

def input_num_con_control(min:int, max:int) -> int:
    seleccion = input("      >>>    ")
    while not seleccion.isnumeric() or int(seleccion)>max or int(seleccion)<min:
        seleccion = input("Inválido. Vuelva a ingresar >>> ")

    seleccion = int(seleccion)
    return seleccion

### ----------------------- AUXILIARES EN SINCRONIZACIÓN ------------------------------------------
###################################################################################################

#### Controlar que canciones ya están en la lista para no repetirlas >>>>>>>>>>>>>>>>>>>


def lista_canciones(info_playlist: dict, lista_cancion: list) -> None:
    artistas:list=list()
    for i in range(len(info_playlist['tracks'])):
        cancion: str = info_playlist['tracks'][i]['name']
        for j in info_playlist['tracks'][i]['artists']:
            artistas.append(j['name'])
        lista_cancion.append([cancion, ','.join(artistas)])

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


#### Parseo de titulos de canciones >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def limpieza_yutub(search: dict) -> list:
    #Recibe un dict con resultados de la búsqueda y devuelve una lista 2d con los resultados parseados
    #lista_encontrados: list = [
    # [id, cancion, cantante],
    # ...]

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
            cantante: str = i['snippet']['channelTitle']
        while '&#39;' in cancion:
            principito: int = cancion.find('&')
            final: int = cancion.find(';')
            apostrofe: str = "'"
            cancion_corregida: str = cancion[0:principito] + apostrofe + cancion[final + 1:len(cancion)]
            cancion = cancion_corregida
        lista_encontrados.append([id, cancion, cantante])
        return lista_encontrados


def spotify_vs_youtube(usuario_actual: dict, spotify: object, token_yutub: object, user_id_spotifai: str,
                       user_id_yutub: str):
    opcion: str = input("Indicar si es de spotify a youtube (1) o"
                        " de youtube a spotify (2)\n >>>")
    # donde se va a guardar la informacion de la lista de spotify
    playlist_spotifai: dict = {}
    detalles_spotifai: dict = {}
    # aca se va a guardar la informacion de la lista de youtube
    playlist_yutub: dict = {}
    detalles_yutub: dict = {}

    # donde se guardaran las uris para pasarlas


    while opcion != "1" and opcion != "2":
        opcion = input("Solo hay dos opciones")
    opcion: int = int(opcion)

    if opcion == 1:
        no_se_pudo: dict = sincronizacion_spotify_a_youtube(usuario_actual, playlist_spotifai, detalles_spotifai,
                                     token_yutub, user_id_yutub, playlist_yutub, detalles_yutub,
                                    spotify)

    else:
        no_se_pudo: dict = sincronizacion_youtube_a_spotify(usuario_actual, playlist_spotifai, detalles_spotifai,
                                       token_yutub, user_id_spotifai,  playlist_yutub,
                                         detalles_yutub, spotify)
    exportar_dict_a_cvs("csv", usuario_actual['name'], no_se_pudo, "no se pudo")


def dame_id_playlist(spotify: object, token_youtube: object, user_id: str, nombre: str, servicio: str)->str:
    if servicio=="spotify":
        playlist = spotify.playlists(user_id, limit=100)
        for i in range(len(playlist.items)):
            if playlist.items[i].name == nombre:
                playlist_id: str = playlist.items[i].id

    elif servicio=="youtube":
        youtube=token_youtube
        request = youtube.playlists().list(
            part="id, snippet",
            mine=True
        )
        response = request.execute()
        print(response)
        for i in response['items']:
            if i['snippet']['title'] == nombre:
                playlist_id: str = i['id']
    return playlist_id


### ----------------------- SINCRONIZACIÓN SPOTIFY A YOUTUBE --------------------------------------
###################################################################################################


def comparacion_con_search_youtube(search: tuple, nombre: str, artista: str,
                                   lista_no_encontrados: list) -> str:
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


def sincronizacion_spotify_a_youtube(usuario_actual: dict, playlist_spotifai: dict, detalles_spotifai: dict,
                                     token_yutub: object, user_id_yutub: str, playlist_yutub : dict,
                                     detalles_yutub: dict, spotify: object) -> dict:
    #DE SPOTIFAI AL YUTUB
    lista_spotifai: list = []
    print_playlists_de_user(usuario_actual, "spotify")
    seleccionar_playlist(usuario_actual, playlist_spotifai, "spotify")
    print(playlist_spotifai)
    # recibo la informacion de la lista elegida
    importar_playlist(spotify, token_yutub, playlist_spotifai['id'],
                      playlist_spotifai['name'],
                      "spotify", detalles_spotifai)
    lista_canciones(detalles_spotifai, lista_spotifai)
    # ahora tengo que saber si quiere crear una nueva o no
    opcion2: str = input("Quiere crear nueva playlist (1) o quiere realizarlo en una ya creada (2)")
    while opcion2 != "1" and opcion2 != "2":
        opcion2 = input("solo hay dos opciones.")
    opcion2: int = int(opcion2)
    if opcion2 == 1:
        # crear lista de youtube
        nombre = crear_playlist_youtube(token_yutub)
        playlist_id = dame_id_playlist(spotify, token_yutub, user_id_yutub, nombre, "youtube")
        lista_yutub: list = []
    else:
        # uso una ya conocida
        lista_yutub: list = []
        print_playlists_de_user(usuario_actual, "youtube")
        seleccionar_playlist(usuario_actual, playlist_yutub, "youtube")
        # recibo la informacion de la lista elegida
        importar_playlist(spotify, token_yutub, playlist_yutub['id'],playlist_yutub['name'],
                          "youtube", detalles_yutub)
        playlist_id: str = detalles_yutub['id']
        lista_canciones(detalles_yutub, lista_yutub)
    lista_agregar: list = comparacion(lista_yutub, lista_spotifai, "spotify")
    lista_no_agregado: list = []
    # uris de las canciones
    for i in lista_agregar:
        search = buscar_item(spotify, token_yutub, "spotify",
                             f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 5, ('track', 'artist'))
        id: str = comparacion_con_search_youtube(search, lista_agregar[i][0], lista_agregar[i][1],
                                       lista_no_agregado)
        if id!="no habemus nada":
            agregar_cancion_a_youtube(playlist_id, id, token_yutub)
    no_se_pudo: dict = {}
    no_se_pudo['no se pudo'] = lista_no_agregado
    return no_se_pudo



### ----------------------- SINCRONIZACIÓN YOUTUBE A SPOTIFY --------------------------------------
###################################################################################################

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
    lista_canciones(detalles_yutub, lista_yutub)
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
        lista_canciones(detalles_spotifai, lista_spotifai)

    elif opcion2 == 2:
        # uso una de las de ahí
        lista_spotifai: list = []
        print_playlists_de_user(usuario_actual, "spotify")
        seleccionar_playlist(usuario_actual, playlist_spotifai, "spotify")
        # recibo la informacion de la lista elegida
        importar_playlist(spotify, token_yutub, playlist_yutub['id'], playlist_yutub['name'],
                          "spotify", detalles_spotifai)
        lista_canciones(detalles_spotifai, lista_spotifai)
    lista_agregar: list = comparacion(lista_yutub, lista_spotifai, "youtube")
    uris: list = []
    lista_no_agregado: list = []
    # uris de las canciones
    for i in lista_agregar:
        search = buscar_item(spotify, token_yutub, "spotify",
                             f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 5, ('track', 'artist'))
        comparacion_con_search_spotify(search, lista_agregar[i][0], lista_agregar[i][1], uris,
                                       lista_no_agregado)
        # se agrega las canciones encontradas
    spotify.playlist_add(playlist_id, uris, position=None)
    no_se_pudo: dict = {}
    no_se_pudo['no se pudo'] = lista_no_agregado
    return no_se_pudo
### ----------------------- WORDCLOUD -------------------------------------------------------------
###################################################################################################


def wordcloud(usuario_actual: dict, spotify: object, token_youtube: object) -> None:
    print("Hola en esta seccion tenemos imagenes de palabras, si desea hacerlo con una playlist\n"
          "de youtube marque (2) de lo contrario (1)")
    opcion: str = input(">>>> ")
    while opcion != "1" and opcion != "2":
        opcion = input(" suspiro..... Vamos de nuevo (1) o (2)")
    opcion: int = int(opcion)

    detalles: dict = {}
    mi_playlist: dict = {}
    if opcion == 1:

        seleccionar_playlist(usuario_actual, mi_playlist,"spotify")
        importar_playlist(spotify, token_youtube, mi_playlist['id'], mi_playlist['name'], "spotify", detalles)
    elif opcion == 2:
        seleccionar_playlist(usuario_actual, mi_playlist, "youtube")
        print("Puede ser que este resultado sea bastate malo, le recomiendo pasar la lista a spotify para un"
              "mejor rendimiento :)")
        importar_playlist(spotify, token_youtube, mi_playlist['id'], mi_playlist['name'], "youtube", detalles)
    letra_total = rejunte_letras(detalles)
    al_wordcloud(letra_total)
    mostrame_esta()


def al_wordcloud(letra_total: str) -> None:
    resp = requests.post('https://quickchart.io/wordcloud', json={
        'format': 'png',
        'width': 1000,
        'height': 1000,
        'fontScale': 15,
        'scale': 'linear',
        'maxNumWords': 10,
        'removeStopwords': True,
        'minWordLength': 4,
        'text': letra_total,
    })

    with open('newscloud.png', 'wb') as f:
        f.write(resp.content)


def mostrame_esta() -> None:
    img = cv.imread('newscloud.png')
    cv.imwrite('modified_img.jpg', img, [int(cv.IMWRITE_JPEG_QUALITY), 100])
    plt.imshow(img)
    plt.show()


### ----------------------- CREAR PLAYLISTS -------------------------------------------------------
###################################################################################################

def crear_playlist_spotify(user_id: str, spotify: object) -> str:
    nombre: str = input("indique el nombre para la playlist en spotify")
    publica: str = input("indique si desea que sea publica (s/n)")
    if publica in "sS":
        public: bool = True
    else:
        public: bool = False
    descripcion: str = input("indique descripción: ")
    spotify.playlist_create(user_id, nombre, public, descripcion)
    return nombre


def crear_playlist_youtube(token_yutub: object) -> str:
    youtube = token_yutub
    nombre: str = input("Indicame el nombre bebe: ")
    descripcion: str = input("La descripcion please")
    privaciti: str = input("Privado (p) o no privado (n) esa es la cuestion")
    i: int = 0
    while privaciti != "p" and privaciti != "n":
        i = i + 1
        if i == 2:
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

def crear_playlist(user_id: str, spotify: object, token_youtube: object)->None:
    print("Usted decidio crear playlist, elija el servidor \n"
          "(1) Spotify\n"
          "(2) Youtube")
    opcion: str = input(">>> ")
    while opcion!="1" and opcion!="2":
        opcion = input("Solo le estoy pidiendo que ingrese numeros no me haga enojar")
    opcion: int = int(opcion)
    if opcion == 1:
        crear_playlist_spotify(user_id, spotify)
    else:
        crear_playlist_youtube(token_youtube)



### ----------------------------- ANALISIS DE PLAYLISTS -------------------------------------------
###################################################################################################

### Funciones reutilizables >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def print_playlists_de_user(usuario_actual:dict, servidor:str) -> None:
    lista_nombres: list = list()
    for playlist in usuario_actual[f'playlists_{servidor}']:
        lista_nombres.append(playlist['name'])
    vis.visual_lista_elementos(lista_nombres, f"Playlists de {servidor}", True)

def playlist_segun_servidor(usuario_actual: dict) -> str:
    print("Desea listar: \n"
          "[1] Playlist de Spotify\n"
          "[2] Playlist de Youtube\n"
          "[3] Mostrar ambas")
    seleccion = input_num_con_control(1,3)

    if seleccion == 1:
        print_playlists_de_user(usuario_actual, "spotify")
        servidor: str = "spotify"
    elif seleccion == 2:
        print_playlists_de_user(usuario_actual, "youtube")
        servidor: str = "youtube"
    else:
        print_playlists_de_user(usuario_actual, "spotify")
        print_playlists_de_user(usuario_actual, "youtube")
        servidor: str = "unknown"
    return servidor


def comprobar_permisos(usuario_actual:dict, servidor:str, seleccion:int) -> bool:
    permitido: bool = False

    if servidor == "spotify":
        id : str= usuario_actual["playlists_spotify"][seleccion - 1]['id']
        if usuario_actual["playlists_spotify"][seleccion - 1]['collaborative']:
            permitido = True
        else:
            spotify = usuario_actual['spotify']
            owner_playlist = spotify.playlist(id).owner
            print(owner_playlist)
            if owner_playlist.id == usuario_actual['id_usuario_spotify']:
                permitido = True
    return permitido



def seleccionar_playlist(usuario_actual:dict, mi_playlist:dict, servidor:str, permisos:bool = False) -> None:
    permitido : bool = False
    print("Seleccione una playlist ")
    seleccion = input("    >>> ")
    while not seleccion.isnumeric() or int(seleccion)<1:
        seleccion = input("Inválido. Vuelva a ingresar >>> ")
    seleccion = int(seleccion)

    if servidor == "spotify" and seleccion>len(usuario_actual['playlists_spotify']):
        print("Número de playlist ingresado inválido.")
    elif servidor == "youtube" and seleccion>len(usuario_actual['playlists_youtube']):
        print("Número de playlist ingresado inválido.")
    else:
        permitido = comprobar_permisos(usuario_actual, servidor, seleccion)
        while servidor == "spotify" and permisos and not permitido:
            print("No puede modificar esa playlist. Elija una suya o que sea colaborativa.")
            seleccion = input_num_con_control(1,len(f'usuario_actual["playlists_{servidor}"]')+1)
            permitido = comprobar_permisos(usuario_actual, servidor, seleccion)

        mi_playlist['servidor'] = servidor
        mi_playlist['name'] = usuario_actual[f"playlists_{servidor}"][seleccion - 1]['name']
        mi_playlist['id'] = usuario_actual[f"playlists_{servidor}"][seleccion - 1]['id']


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

    info_playlist:list=list()
    if servidor == "spotify":
        info_playlist.append(Spotify.playlist(spotify, playlist_id, fields=None, market=None, as_tracks=True))

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

def analizar_track(track:dict, atributos_track:dict, spotify:object, atributos:list, servidor:str='spotify') -> None:
    if servidor == "spotify":
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
    servidor:str = playlist_segun_servidor(usuario_actual)
    if servidor == "unknown":
        servidor = seleccion_servidor()

    seleccionar_playlist(usuario_actual, mi_playlist, servidor)

    if mi_playlist['servidor'] == "spotify":
        importar_playlist(usuario_actual['spotify'], usuario_actual['token_youtube'], mi_playlist['id'],
                          mi_playlist['name'], mi_playlist['servidor'], detalles_playlist)
        for track in detalles_playlist['tracks']:
            try:
                analizar_track(track, atributos_track, usuario_actual['spotify'], atributos)
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
                exportar_dict_a_cvs('cvs', usuario_actual['username'], atributos_playlist,
                                    f"atributos_playlist_{mi_playlist['id']}")
            except TimeoutError:
                print(vis.NO_INTERNET)

        if os.path.isfile(f'atributos_playlist_{mi_playlist["id"]}_{usuario_actual["username"]}.cvs'):
            print(f"Se ha creado un archivo con los atributos de la playlist {atributos_playlist['playlist name']} \n"
                  f"en el directorio {os.getcwd()}")
        else:
            print("Ha habitado un error al generar el archivo. Intentelo nuevamente.")

    else:
        print("No podemos realizar un analisis de atributos musicales para"
              " playlists en youtube.") #Youtube Music API when ??
        print("Le ofrecemos:"
              "[1] Sincronizar esta playlist con spotify y realizar el analisis de las canciones coincidentes.")
        print("[2] Dar un informe sobre los datos principales de esta playlist al momento.")


### ------------------------ BÚSQUEDA DE CANCIONES ------------------------------------------------
###################################################################################################

def seleccion_servidor() -> str:
    servidor = input("Ingrese el servidor en el que desea buscar: ").lower()
    while not servidor == "spotify" and not servidor == "youtube":
        servidor = input("Servidor inválido, vuelva a ingresar >>> ").lower()
    return servidor

def buscar_cancion(spotify: object, token_youtube: str, resultados: list, servidor:str) -> None:
    datos_parseados : list = list()
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

    cancion = input("Ingrese el nombre de la canción a buscar >>> ")
    artista = input("Ingrese el artista >>> ")
    search = buscar_item(spotify, token_youtube, servidor, f"{cancion} {artista}", 3, ('track', ))
    # search = buscar_item(spotify, token_youtube, servidor, f"{cancion}, {artista}", 3, ('track', 'artist'))

    if servidor == "spotify":
        print("Buscando en spotify...")
        for x in search:  # tupla #object
            for item in x.items:
                item_n: dict = dict()
                item_n['id'] = item.id
                item_n['name'] = item.name
                item_n['uri'] = item.uri
                try:
                    item_n['artists'] = []
                    for artist in item.album.artists:  # artists es lista en model
                        item_n['artists'].append(artist.name)
                except AttributeError:
                    item_n['album'] = "Desconocido"
                try:
                    item_n['album'] = item.album.name
                except AttributeError:
                    item_n['artists'] = "Desconocido"
                resultados.append(item_n)

    elif servidor == "youtube":
        print("Buscando en youtube...")
        for x in search['items']:  # dict
            item_n: dict = dict()
            item_n['id'] = x['id']['videoId']
            item_n['name'] = x['snippet']['title']
            item_n['artists'] = [x['snippet']['channelTitle']]
            item_n['album'] = "Desconocido"
            resultados.append(item_n)



def buscar_item(spotify:object, token_youtube:object, servidor:str, query:str, limit:int, types:tuple=('track',))-> None:
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



### ------------------------ ACCIONES POSTERIORES A BÚSQUEDA --------------------------------------
###################################################################################################

def agregar_cancion_a_youtube(playlist_id:str, cancion_id:str, youtube:object) -> None:
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


def agregar_a_playlist(usuario_actual:dict, cancion:dict, servidor:str) -> None:
    mi_playlist: dict = dict()

    seleccionar_playlist(usuario_actual, mi_playlist, servidor, True)
    if mi_playlist['servidor'] == 'spotify':
        agregar_cancion_a_spotify(mi_playlist['id'], cancion['uri'], usuario_actual['spotify'])
    elif mi_playlist['servidor'] == 'youtube':
        agregar_cancion_a_youtube(mi_playlist['id'], cancion['id'], usuario_actual['token_youtube'])


def agregar_cancion_a_spotify(playlist_id:str, uri_cancion:list, spotify:object) -> None:
    try:
        spotify.playlist_add(playlist_id, uri_cancion, position=None)
        print("Canción agregada correctamente")
    except TimeoutError:
        print(vis.NO_INTERNET)



def info_html_de_youtube(cancion:dict) -> None:
    track: str =""
    artista: str = ""
    try:
        url = f"https://www.youtube.com/watch?v={cancion['id']}"
        ydl = youtube_dl.YoutubeDL({})
        with ydl:
            video = ydl.extract_info(url, download=False)
            if video != {}:
                track = video['track']
                artista = video['artist']
            else:
                print("No pudimos extraer información del track por este medio.")
    except KeyError:
        print("Error en el sistema. No se pudo extraer por este medio.")

    return track, artista


def visualizar_cancion(cancion: dict, seleccion: int, servidor:str) -> None:
    nombre = cancion['name']
    artistas: str = ','.join(cancion['artists'])

    vis.mostrar_cancion(cancion, seleccion)
    token_genius: str = ingreso_genius()
    letra: str = extraer_letra(token_genius, nombre, artistas)
    if letra == "":
        print("No se ha encontrado ninguna letra para esta canción.")
        print("\n- [x] Si quiere buscar la letra por otros medios"
              "\n- Cualquier [Tecla] para finalizar")
    else:
        print(letra)
        print("\n- [x] Si la letra mostrada es incorrecta y quiere "
                        "volver a buscarla\n- Cualquier [Tecla] para finalizar")

    es_la_letra = input("     >>>   ")
    if es_la_letra in "xX":
        if servidor == "youtube":
            print("[1] Ingresar nombre manualmente \n"
                  "[2] Extraer información con la libreria youtube_dl")
            opcion:int=input_num_con_control(1,2)
            if opcion == 1:
                letra = extraer_letra(token_genius)
            else:
                nombre, artistas = info_html_de_youtube(cancion)
                if nombre != "" and artistas!= "":
                    print(f"Encontramos que la canción es {nombre}\n por {artistas}")
                    letra = extraer_letra(token_genius, nombre, artistas)
        else:
            print("Puede probar ingresando el nombre manualmente. ")
            letra = extraer_letra(token_genius)

        if letra == "":
            print("No pudimos encontrar la letra que buscaba. ")
        else:
            print(letra)

        input("Presione una tecla para volver al menu >>> ")


def administracion_de_canciones(usuario_actual:dict) -> None:
    resultados: list = list()
    titulo: str = "Administrar canción"
    opciones: list = [
        "Visualizar", "Agregar a playlist"
    ]

    servidor = seleccion_servidor()
    buscar_cancion(usuario_actual['spotify'], usuario_actual['token_youtube'], resultados, servidor)
    if len(resultados) > 0:
        print(f"""\n     Resultados de búsqueda""")
        for i in range(len(resultados)):
            if servidor == "spotify":
                vis.mostrar_cancion(resultados[i], i+1)
            elif servidor == "youtube":
                vis.mostrar_nombre_vid(resultados[i], i+1)

        print("Ingrese el codigo de la canción que buscaba")
        seleccion_cancion = input_num_con_control(1,3)

        vis.menu_con_opciones_cortas(titulo, opciones)
        accion = input_num_con_control(1,(len(resultados)+1))

        if accion == 1:
            visualizar_cancion(resultados[seleccion_cancion-1], seleccion_cancion, servidor)
        else:
            print("Vamos a elegir una playlist de la lista")
            print_playlists_de_user(usuario_actual, servidor)
            agregar_a_playlist(usuario_actual, resultados[seleccion_cancion-1], servidor)
    else:
        print("No hemos obtenido ningún resultado de la búsqueda")


###------------------------- MANEJO DE LYRICS ------------------------------------------------------
####################################################################################################
def ingreso_genius()->str:
    client_id: str = "LkrBCrYXlZO4Wm7Hx1X-AU0g9z_bNYc2ehowpFLNhgcVa-MdX8J1zceedRf59FNN"
    client_secret: str = "nRzbwpwEiEcic8uN9qyXRKAwo8O2e48lstan5rtc8F8FKIw6QbY1DUGV8P_FTzom763BRHuJWKcowt7jm9U8mQ"
    token_genius: str = "OomA5Dwkt15uqiCNHKthDcDx7gqYbFAkXeQFoX_DHqu-C6NQzyuBoxOY5o76C64P"
    return token_genius


def extraer_letra(token_genius, cancion: str = "0", artista: str = "0") -> str:
    ser_o_no_ser: str = "aun no paso nada"
    genius = Genius(token_genius)
    # saca los headers
    genius.remove_section_headers = True
    # Exclude songs with these words in their title
    genius.excluded_terms = ["(Remix)", "(Live)", "(Cover)"]
    # Turn off status messages
    genius.verbose = False

    if cancion == "0" and artista == "0":
        #Si queremos que el usuario busque el nombre de la canción manualmente
        es_cancion: bool = False
        while es_cancion == False:
            cancion = input("Nombre del cantante:")
            artista = input("Nombre de canción: ")
            song = genius.search_song(cancion, artista)
            print(song)
            print("¿Es la canción que usted busca? "
                  "[s] Si "
                  "[n] No "
                  "[x] dejar de buscar")
            ser_o_no_ser = input(">>> ").lower()
            if ser_o_no_ser == "s":
                es_cancion = True
            elif ser_o_no_ser == "x":
                print("Trabajaremos para mejorar la base de datos de canciones.")
                es_cancion = True
            else:
                es_cancion = False
    else:
        song = genius.search_song(cancion, artista)

    if ser_o_no_ser != "x":
        try:
            letra_song: str = str(song.lyrics)
        except AttributeError:
            letra_song: str = ""
    return letra_song


def rejunte_letras(detalles: dict) -> str:
    token_genius = ingreso_genius()
    total_letrasas: str = ""
    for cancioncita in range(len(detalles['tracks'])):
        letra: str = extraer_letra(token_genius, detalles['tracks'][cancioncita]['name'],
                                   detalles['tracks'][cancioncita]['artists'])
        total_letrasas = total_letrasas + letra
    return total_letrasas


###------------------------- LISTADO DE PLAYLISTS  -------------------------------------------------
####################################################################################################


def playlists_spotify(spotify, id_usuario) -> None:
    datos_playlists = spotify.playlists(id_usuario)
    nombres = [x.name for x in datos_playlists.items]
    if nombres:
        vis.visual_lista_elementos(nombres, "Playlists de Spotify", True)
    else:
        print(vis.NO_PLAYLIST)


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


#### ----------------------------- MANEJO DE PERFILES ----------------------------------------------
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


def guardar_spotify_en_json(nombre: str, refresh_token: str = "") -> None:
    """Guarda los datos recibidos en un archivo json (si no existe, se crea aqui)."""
    datos_existentes: dict = {}
    perfil_a_guardar: dict = {nombre: {"spotify": refresh_token}}
    if os.path.isfile("datos_perfiles.json"):
        datos_existentes: dict = sacar_info_json("datos_perfiles.json")
    datos_existentes.update(perfil_a_guardar)
    escribir_json(datos_existentes, "datos_perfiles.json")


def nombres_perfiles_guardados() -> list:
    """Devuelve los nombres que estan el archivo json de los perfiles, si no lo encuentra devuelve una lista vacia."""
    if not os.path.isfile("datos_perfiles.json"):
        return []
    with open("datos_perfiles.json") as f:
        datos = json.load(f)
        return list(datos.keys())


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


def nuevo_perfil():
    """Guarda el perfil solo si acepto los permisos de al menos una plataforma."""
    nombre: str = nombre_perfil()
    opciones_elegidas: list = []
    terminar: bool = False
    while not terminar:
        vis.youtube_spotify(True, opciones_elegidas)
        opcion = input_num_con_control(1,3)
        if opcion == 1:
            pass
            # obj_youtube = autenticarYT()
            # opciones_elegidas.append(opcion)
        elif opcion == 2:
            refresh_token: str = autenticar_spotify()
            if refresh_token:
                opciones_elegidas.append(opcion)   # REVISAR EL APPEND, QUE PASA SI EL USUARIO USA ESTO 2 VECES
        elif opcion == 3 and opciones_elegidas:
            guardar_spotify_en_json(nombre, refresh_token)
            print(vis.DATOS_GUARDADOS)
            terminar: bool = True
        else:
            terminar: bool = True


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
    # numeros_permitidos: list = [x for x in range(1,len(nombres_perfiles)+1)]
    opcion = input_num_con_control(1,len(nombres_perfiles))
    if opcion == len(nombres_perfiles):
        return perfil_elegido
    if perfil["username"] and perfil["username"] == nombres_perfiles[opcion-1]:   # CUANDO VUELVE A ELEGIR PERFIL, PARA QUE NO ELIJA EL MISMO
        return perfil_elegido
    perfil_elegido: str = nombres_perfiles[opcion-1]
    return perfil_elegido


def manejo_perfiles(perfil: dict):
    """
    Genera un menu para crear y guardar perfiles junto con la opcion de elegir uno de los perfiles guardados.
    Si eligio un perfil entonces el nombre se guardara en el diccionario recibido.
    """
    terminar: bool = False
    while not terminar:
        vis.menu_perfiles(perfil["username"])
        # opcion: int = opciones([1, 2, 3])
        opcion = input_num_con_control(1,3)
        if opcion == 1:
            perfil_elegido: str = elegir_perfil(perfil)                             # EN REVISION
            if perfil_elegido:
                perfil["username"] = perfil_elegido
        elif opcion == 2:
            nuevo_perfil()
        else:
            terminar: bool = True

#### ----------------------------- AUTENTICACIÓN SPOTIFY ------------------------------------------
###################################################################################################

def autenticar_spotify() -> str:
    """Devuelve un refresh_token si la autenticacion salio bien, caso contrario devuelve un string vacio."""
    refresh_token: str = ""
    credenciales: tk.RefreshingCredentials = tk.RefreshingCredentials(ID_CLIENTE, CLIENTE_SECRETO, URI_REDIRECCION)
    auth: tk.UserAuth = tk.UserAuth(credenciales, SCOPE)
    print(vis.INSTRUCCIONES)
    input("Presione Enter para que se abra Spotify: ")
    web_open(auth.url)
    print()
    print("Aqui abajo debes ingresar la URL que copiaste:  ")
    url: str = input("--->  ").strip()
    try:
        token: tk.RefreshingToken = auth.request_token(url=url)
    except KeyError:
        print(vis.ERROR_URL)
    else:
        refresh_token: str = token.refresh_token
        print(vis.DATOS_GUARDADOS)
    return refresh_token

#### ----------------------------- AGREGAR DATOS DE SPOTIFY AL PERFIL -----------------------------
###################################################################################################

def obtener_refresh_token_perfil(nombre: str) -> str:
    """Devuelve el refresh_token del nombre recibido, si el archivo de donde lo saca no esta entonces devuelve un str vacio."""
    if not os.path.isfile("datos_perfiles.json"):
        return ""
    with open("datos_perfiles.json") as f:
        datos = json.load(f)
    return datos[nombre]["spotify"]


def conseguir_datos_playlists(spotify, id_usuario):
    """
    Pre: Recibe un objeto spotify (ya con los datos de nuestro perfil elegido) y el id de Spotify del perfil actual.
    Post: Devuelve una lista con un monton de datos de las playlists que tiene el perfil actual.
    """
    datos = []
    datos_playlists = spotify.playlists(id_usuario)  # Que pasa si el usuario no tiene playlists?
    for playlist in datos_playlists.items:
        diccionario: dict = {}                  # Deberia cambiarle el nombre.
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


def datos_necesarios_perfil(perfil: dict) -> None:  # NECESITO INFORMACION DE YOUTUBE
    """
    Pre: Recibe un diccionario solo con el nombre del perfil.
    Post: Le agrega datos, como por ejemplo id, playlists, al diccionario recibido.
    """
    refresh_token = obtener_refresh_token_perfil(perfil["username"])
    if refresh_token:
        token = tk.refresh_user_token(ID_CLIENTE, CLIENTE_SECRETO, refresh_token)
        spotify = tk.Spotify(token)
        perfil["spotify"] = spotify
    if "spotify" in perfil:
        id_usuario = spotify.current_user().id
        perfil["id_usuario_spotify"] = id_usuario
    if "spotify" in perfil and "id_usuario_spotify" in perfil:
        datos_playlists: list = conseguir_datos_playlists(perfil["spotify"], perfil["id_usuario_spotify"])
        perfil["playlists_spotify"] = datos_playlists


def datos_agregados_correctamente(usuario_actual: dict) -> bool:   # NECESITO INFORMACION DE YOUTUBE
    """
    Pre: Recibe un diccionario con los datos del perfil actual.
    Post: Devuelve un False si encuentra que falta un dato importante.
    """
    if not usuario_actual["username"]:
        return False
    datos_necesarios_perfil(usuario_actual)
    if "spotify" not in usuario_actual:
        return False
    elif "id_usuario_spotify" not in usuario_actual:
        return False
    elif "playlists_spotify" not in usuario_actual:
        return False
    elif "playlists_youtube" not in usuario_actual:
        return False
    return True


#### ----------------------------- AUTENTICACIÓN YOUTUBE ------------------------------------------
###################################################################################################

def validar_permisosYT(usuario: str, youtube: object) -> object:
    with open("datos_perfiles_YT.json", "r") as f:
        datos: dict = json.load(f)

    # Me guardo las claves que generó el usuario del perfil para YouTube.
    claves: dict = datos[usuario]["youtube"]

    # Recupero los permisos.
    permisos = google.oauth2.credentials.Credentials(
        token=claves["token"], refresh_token=claves["refresh_token"],  # id_token=id_token,
        token_uri=claves["token_uri"], client_id=claves["client_id"],
        client_secret=claves["client_secret"], scopes=claves["scopes"]
    )

    # Verifico si son válidos.
    if (permisos.expired == False):
        # Solicito nuevos permisos y refresco los existentes.
        solicitar = google.auth.transport.requests.Request()
        permisos.refresh(solicitar)

        # Los guardo en el archivo de credenciales de perfiles.
        dicc: dict = {usuario: {"youtube": json.loads(permisos.to_json())}}
        with open("datos_perfiles_YT.json", "w") as f:
            json.dump(dicc, f)

        # Genero un nuevo cliente de YouTube.
        api_service_name: str = "youtube"
        api_version: str = "v3"
        youtube: object = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=permisos
        )

        return youtube
    else:
        return youtube


def autenticarYT(usuario: str) -> object:
    scopes = ["https://www.googleapis.com/auth/youtube"]

    # Verificación HTTPS OAuthlib activada.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name: str = "youtube"
    api_version: str = "v3"
    client_secrets_file: str = "credenciales_YT.json"

    # Autorización.
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    permisos = flow.run_console()

    # Creo un cliente API para hacer solicitudes.
    clienteYT: object = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=permisos
    )

    # Guardo los permisos otorgados.
    dicc: dict = {usuario: {"youtube": json.loads(permisos.to_json())}}
    with open("datos_perfiles_YT.json", "w") as f:
        json.dump(dicc, f)

    return clienteYT

def id_canal_youtube(youtube:object) -> None:
    request = youtube.channels().list(
            part= "id",
            mine= True
            )
    response = request.execute()["items"] #Devuelve una lista con la información del canal.
    id_YT: str = response[0]["id"]
    return id_YT

####################################################################################################
####################################################################################################


def main() -> None:
  
    vis.inicio()
    usuario_actual: dict = {"username": ""}
    manejo_perfiles(usuario_actual)

    terminar: bool = True
    if datos_agregados_correctamente(usuario_actual):
        terminar: bool = False

    #########PROVISORIO PARA PROBAR YOUTUBE##############
    usuario_actual['token_youtube'] = autenticarYT(usuario_actual['username'])
    usuario_actual['playlists_youtube'] = listar_playlistsYT(usuario_actual['token_youtube'])
    usuario_actual['id_usuario_youtube'] = id_canal_youtube(usuario_actual['token_youtube'])

    # usuario_actual: dict= {
    #     'username': str,
    #     'spotify' : object,
    #     'youtube' : object,
    #     'playlists_youtube' : list,
    #     'playlists_spotify' : list
    # }

    ##### --------MENU PRINCIPAL DENTRO DEL PERFIL--------------------------

    seleccion = 9876543210
    while seleccion != 0:
        print(vis.MENU)
        seleccion = input_num_con_control(0, 7)
        if seleccion == 1:
            #Listar las playlist
            playlist_segun_servidor(usuario_actual)
        elif seleccion == 2:
            #Exportar analisis de playlist a CSV
            analisis_de_playlist(usuario_actual)
        elif seleccion == 3:
            # Crear playlist
            crear_playlist(usuario_actual['id_usuario_spotify'], usuario_actual['spotify'],
                           usuario_actual['token_youtube'])
        elif seleccion == 4:
            #Buscar y administrar canción
            administracion_de_canciones(usuario_actual)
        elif seleccion == 5:
            #Sincronizar playlists
            spotify_vs_youtube(usuario_actual, usuario_actual['spotify'], usuario_actual['token_youtube'],
                               usuario_actual['id_usuario_spotify'], usuario_actual['id_usuario_youtube'])
        elif seleccion == 6:
            #Generar wordcloud
            wordcloud(usuario_actual, usuario_actual['spotify'], usuario_actual['token_youtube'])
        elif seleccion == 7:
            #Cambiar de perfil
            manejo_perfiles(usuario_actual)

main()
