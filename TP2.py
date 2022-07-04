import matplotlib.pyplot as plt
import cv2 as cv
import tekore as tk
from tekore import Spotify
import requests
from lyricsgenius import Genius
import csv
import os
from datetime import date
import json
import youtube_dl
import TP2_PERFILES as perf
import TP2_VISUAL as vis

###################################################################################################

def input_num_con_control(min:int, max:int) -> int:
    #Recibo el rango de opciones para un menu numerico
    #Devuelve una opción en ese rango como int
    seleccion = input("      >>>    ")
    while not seleccion.isnumeric() or int(seleccion) > max or int(seleccion) < min:
        seleccion = input("Inválido. Vuelva a ingresar >>> ")
    seleccion = int(seleccion)
    return seleccion

### ----------------------- CONSEGUIR PLAYLISTS (YT/SP) -------------------------------------------
###################################################################################################

def listar_playlistsYT(youtube: object) -> dict:
    """ Recupera la data de todas las playlists que tiene un usuario en Youtube """
    request = youtube.playlists().list(
                    part="snippet,id,status,contentDetails",
                    maxResults=50,
                    mine=True
                    )
    response = request.execute()
    # En caso de que haya más de 50 resultados: 
    nextPageToken = response.get("nextPageToken")
    while ("nextPageToken" in response):
        nextPage = youtube.playlists().list(
                        part="snippet",
                        maxResults="50",
                        pageToken=nextPageToken
                        ).execute()
        response["items"] = response["items"] + nextPage["items"]

        if "nextPageToken" not in nextPage:
            response.pop("nextPageToken", None)
        else:
            nextPageToken = nextPage["nextPageToken"]
    return response['items']

def ordenar_datos_playlist_YT(playlist) -> dict:
    """Recibe un objeto con los datos de la playlist y devuelvo un diccionario solo con los que necesitamos."""
    datos_playlist: dict = {}
    datos_playlist["nombre"] = playlist["snippet"]["title"]
    datos_playlist["id"] = playlist["id"]
    datos_playlist["collaborative"] = playlist["status"]["privacyStatus"]
    datos_dueño_playlist: dict = {
        "nombre": playlist["snippet"]["channelTitle"],
        "id": playlist["snippet"]["channelId"],
        "uri": "desconocido"
    }
    datos_playlist["dueño"] = datos_dueño_playlist
    datos_playlist["cant_tracks"] = playlist["contentDetails"]["itemCount"]
    return datos_playlist    


def datos_playlists_YT(youtube: object) -> list:
    """ Consigue el id, nombre, descripción y estado (publica o privada) de todas las playlists 
    del usuario para el que se haya solicitado """
    datos: list = []
    data_response: dict = listar_playlistsYT(youtube)
    for i in range(len(data_response)):
        datos_playlist: dict = ordenar_datos_playlist_YT(data_response[i])
        datos.append(datos_playlist)
    return datos


def ordenar_datos_playlist_SP(playlist) -> dict:            # Falta typing
    """Recibe un objeto con los datos de la playlist y devuelvo un diccionario solo con los que necesitamos."""
    datos_playlist: dict = {}
    datos_playlist["nombre"] = playlist.name
    datos_playlist["id"] = playlist.id
    datos_playlist["collaborative"] = playlist.collaborative
    datos_dueño_playlist: dict = {
        "nombre": playlist.owner.display_name,
        "id": playlist.owner.id,
        "uri": playlist.owner.uri
    }
    datos_playlist["dueño"] = datos_dueño_playlist
    datos_playlist["cant_tracks"] = playlist.tracks.total
    return datos_playlist


def datos_playlists_SP(spotify: tk.Spotify, id_usuario: str) -> list:
    """
    Pre: Recibe un objeto spotify (ya con los datos de nuestro perfil elegido) y el id de Spotify del perfil actual.
    Post: Devuelve una lista con un monton de datos de las playlists que tiene el perfil actual.
    """
    datos: list = []
    datos_playlists: list = perf.probando(spotify.playlists, [id_usuario, 50])
    if datos_playlists and datos_playlists[0].items:  # Si hay playlists
        for playlist in datos_playlists[0].items:
            datos_playlist: dict = ordenar_datos_playlist_SP(playlist)
            datos.append(datos_playlist)
    elif not datos_playlists:
        datos.append("SIN INTERNET")
    return datos

### ----------------------- AUXILIARES EN SINCRONIZACIÓN ------------------------------------------
###################################################################################################

#### Controlar que canciones ya están en la lista para no repetirlas >>>>>>>>>>>>>>>>>>>

def lista_canciones(info_playlist: dict, lista_cancion: list, servidor: str) -> None:
    # Lista las canciones para poder comparar si hay alguna, para que no se repitan
    if servidor == "spotify":
        for i in range(len(info_playlist['tracks'])):
            # los artistas pueden ser varios por lo que se genera una lista
            artistas: list = []
            cancion: str = info_playlist['tracks'][i]['name']
            for j in range(len(info_playlist['tracks'][i]['artists'])):
                artistas.append(info_playlist['tracks'][i]['artists'][j]['name'])
            # por cada track se agrega en nombre de la canción y los artistas
            lista_cancion.append([cancion, ','.join(artistas)])
    if servidor == "youtube":
        # la misma función pero para youtubr
        for i in range(len(info_playlist['tracks'])):

            cancion: str = info_playlist['tracks'][i]['name']
            artistas = (info_playlist['tracks'][i]['artists'])
            cancioncita: str = ""
            artistis: str = ""
            # se intenta limpiar el nombre para poder encontrarlo en spotify
            cancioncita, artistis = limpieza(cancion, artistas)
            lista_cancion.append([cancioncita, artistis])


def comparacion(lista_yutub: list, lista_spotifai: list, servicio_base: str) -> list:
    # comparar ambas listas para no agregar repetidos
    lista_a_agregar: list = []
    if servicio_base == "spotify":
        # si es desde spotify a youtube se realiza la comparación agregando aquelloras de spotify que no
        # encuentren par con la lista en youtube
        for i in range(len(lista_spotifai)):
            esta: bool = False
            for j in range(len(lista_yutub)):
                if lista_spotifai[i] == lista_yutub[j]:
                    esta = True
            if esta == False:
                lista_a_agregar.append(lista_spotifai[i])
    if servicio_base == "youtube":
        # lo mismo pero para youtube
        for i in range(len(lista_yutub)):
            esta: bool = False
            for j in range(len(lista_spotifai)):
                if lista_yutub[i] == lista_spotifai[j]:
                    esta = True
            if esta == False:
                lista_a_agregar.append(lista_yutub[i])
    print(lista_a_agregar)
    return lista_a_agregar


#### Parseo de titulos de canciones >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def limpieza_yutub(search: dict) -> list:
    # cuando hay un search debo ordenar la información
    lista_encontrados: list = []
    for i in search['items']:
        # se recorre
        # titulo real del video
        titulo: str = i['snippet']['title']
        id: str = i['id']['videoId']
        cancion: str = ""
        cantante:  str = ""
        cancion,cantante = limpieza(titulo, search['items'][0]['channelTitle'])
        lista_encontrados.append([id, cancion, cantante])
    return lista_encontrados


def limpieza(titulo: str, canal: str) -> tuple:
    # se intenta corregir los nombres que provienen de youtube ya que estos no son compatibles con spotify
    # cuando salen comillas normalmente es el nombre de la canción
    if "&#39;" in titulo:
        star: int = titulo.find('&')
        comienzo: int = titulo.find(';')
        cantante = titulo[0:star]
        cancion: str = titulo[comienzo + 1:len(titulo)]
        fin: int = cancion.find('&#39; ')
        cancion = cancion[0:fin]

    # forma del pop
    # normalmente tienen esta separación
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
        cantante: str = canal
    # los apostrofes en canciones en ingles
    while '&#39;' in cancion:
        principito: int = cancion.find('&')
        final: int = cancion.find(';')
        apostrofe: str = "'"
        cancion_corregida: str = cancion[0:principito] + apostrofe + cancion[final + 1:len(cancion)]
        cancion = cancion_corregida
    return (cancion, cantante)


def spotify_vs_youtube(usuario_actual: dict, spotify: object, token_yutub: object, user_id_spotifai: str,
                       user_id_yutub: str) -> None:
    opcion: str = input("Indicar si es de spotify a youtube (1) o"
                        " de youtube a spotify (2)\n >>>")
    # donde se va a guardar la informacion de la lista de spotify
    playlist_spotifai: dict = {}
    detalles_spotifai: dict = {}
    # aca se va a guardar la informacion de la lista de youtube
    playlist_yutub: dict = {}
    detalles_yutub: dict = {}

    while opcion != "1" and opcion != "2":
        opcion = input("Solo hay dos opciones: ")
    opcion: int = int(opcion)

    if opcion == 1:
        no_se_pudo: dict = sincronizacion_spotify_a_youtube(usuario_actual, playlist_spotifai, detalles_spotifai,
                                     token_yutub, user_id_yutub, playlist_yutub, detalles_yutub,
                                    spotify)
    else:
        no_se_pudo: dict = sincronizacion_youtube_a_spotify(usuario_actual, playlist_spotifai, detalles_spotifai,
                                       token_yutub, user_id_spotifai,  playlist_yutub,
                                         detalles_yutub, spotify)
    # si hay algo en el dict de no se pudo se exporta a csv sino un cartel
    if len(no_se_pudo['no se pudo']) != 0:
        exportar_dict_a_csv("csv", usuario_actual['username'], no_se_pudo, "no se pudo")
    else:
        print("HABEMUS UN GANADOR, USTED PASO TODAS SUS CANCIONES CORRECTAMENTE")


def dame_id_playlist(spotify: object, token_youtube: object, user_id: str, nombre: str, servicio: str) -> str:
    # cuando se crea playlist y no se sabe el id de la cancion

    playlist_id: str =""
    if servicio=="spotify":
        # se busca en las playlist cual tiene el mismo nombre y se da el id
        playlist = spotify.playlists(user_id, limit=50)
        for i in range(len(playlist.items)):
            if playlist.items[i].name == nombre:
                playlist_id = playlist.items[i].id

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
                playlist_id = i['id']
    return playlist_id

### ----------------------- SINCRONIZACIÓN SPOTIFY A YOUTUBE --------------------------------------
###################################################################################################

def comparacion_con_search_youtube(search: tuple, nombre: str, artista: str,
                                   lista_no_encontrados: list) -> str:
    # se ve si se encontro algo o no y se da el id.
    id_elegido: str = ""
    if len(search) != 0:
        for i in search['items']:
            id_elegido = i['id']['videoId']
    else:
        id_elegido = "no habemus nada"
        lista_no_encontrados.append([nombre, artista])
    return id_elegido


def sincronizacion_spotify_a_youtube(usuario_actual: dict, playlist_spotifai: dict, detalles_spotifai: dict,
                                     token_yutub: object, user_id_yutub: str, playlist_yutub: dict,
                                     detalles_yutub: dict, spotify: object) -> dict:
    # DE SPOTIFAI AL YUTUB
    lista_spotifai: list = []
    print_playlists_de_user(usuario_actual, "spotify")  # poner un if not usuario_actual["spotify"]["playlists_spotify"]
    seleccionar_playlist(usuario_actual, playlist_spotifai, "spotify") # Para que no llegue aqui si no hay ninguna playlist
    # recibo la informacion de la lista elegida
    importar_playlist(spotify, token_yutub, playlist_spotifai['id'],
                      playlist_spotifai['name'],
                      "spotify", detalles_spotifai)
    lista_canciones(detalles_spotifai, lista_spotifai, "spotify")
    # ahora tengo que saber si quiere crear una nueva o no
    opcion2: str = input("Quiere: \n [1] crear nueva playlist \n [2] realizarlo en una ya creada ")
    while opcion2 != "1" and opcion2 != "2":
        opcion2 = input("Solo hay dos opciones: ")
    opcion2: int = int(opcion2)
    if opcion2 == 1:
        # crear lista de youtube
        nombre, playlist_id = crear_playlist_youtube(token_yutub)
        #playlist_id: str = ""
        # se obtiene el id
        #playlist_id = dame_id_playlist(spotify, token_yutub, user_id_yutub, nombre, "youtube")
        # la lista de canciones es nula
        lista_yutub: list = []
    else:
        # uso una ya conocida
        lista_yutub: list = []
        print_playlists_de_user(usuario_actual, "youtube")
        seleccionar_playlist(usuario_actual, playlist_yutub, "youtube", True)
        # recibo la informacion de la lista elegida
        importar_playlist(spotify, token_yutub, playlist_yutub['id'], playlist_yutub['name'],
                          "youtube", detalles_yutub)
        playlist_id: str = detalles_yutub['id']
        # la lista de canciones se desconoce (en forma de lista) por lo que llamo a la función
        lista_canciones(detalles_yutub, lista_yutub, "youtube")
    # comparo cuales debo agregar y cuales no
    lista_agregar = comparacion(lista_yutub, lista_spotifai, "spotify")
    # es la lista de aquellos que no se puede
    lista_no_agregado: list = []
    for i in range(len(lista_agregar)):
        search = buscar_item(spotify, token_yutub, "youtube",
                             f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 1, ('track',))
        id: str = comparacion_con_search_youtube(search, lista_agregar[i][0], lista_agregar[i][1],
                                                 lista_no_agregado)
        # se busca y se obtiene el id, si no hay ningun id el comparacion con search entrega un id con las palabras no habemus nada
        if id != "no habemus nada":
            # se agrega canción por canción
            agregar_cancion_a_youtube(playlist_id, id, token_yutub)
    no_se_pudo: dict = {}
    no_se_pudo['no se pudo'] = lista_no_agregado
    return no_se_pudo

### ----------------------- SINCRONIZACIÓN YOUTUBE A SPOTIFY --------------------------------------
###################################################################################################

def comparacion_con_search_spotify(search: tuple, nombre: str, artista: str, uris: list,
                                   lista_no_encontrados: list) -> None:
    # limpio el search y si no se encontro se suma a los no encontrados.
    # es más posible que esto suceda ya que puede haber cosas en las listas de youtube que no es música
    if len(search) !=0 :
        for x in search:
            for item in x.items:
                uris.append(item.uri)
    else:
        lista_no_encontrados.append([nombre, artista])


def sincronizacion_youtube_a_spotify(usuario_actual: dict, playlist_spotifai: dict, detalles_spotifai: dict,
                                     token_yutub: object, user_id_spotifai: str, playlist_yutub: dict,
                                     detalles_yutub: dict, spotify: object, emergencia:bool= False) -> dict:
    # A ESTE PUNTO LA PROGRAMADORA SE ESTA PREGUNTANDO SI ES BUENA IDEA SEGUIR VIVIENDO
    playlist_id: str = ""
    lista_yutub: list = []
    # youtube a spotify
    if not emergencia:
        print_playlists_de_user(usuario_actual, "youtube")
        seleccionar_playlist(usuario_actual, playlist_yutub, "youtube")

    # recibo la informacion de la lista elegida
    importar_playlist(spotify, token_yutub, playlist_yutub['id'], playlist_yutub['name'],
                      "youtube", detalles_yutub)
    # busco las canciones en la lista que eleji de youtube
    lista_canciones(detalles_yutub, lista_yutub, "youtube")
    opcion2: str = input("Quiere: \n [1] crear nueva playlist \n [2] realizarlo en una ya creada ")
    while opcion2 != "1" and opcion2 != "2":
        opcion2 = input("Solo hay dos opciones: ")
    opcion2: int = int(opcion2)
    if opcion2 == 1:
        # creo la playlist de spotify
        # la lista de canciones es nula
        lista_spotifai: list = []
        nombre, playlist_id = crear_playlist_spotify(usuario_actual)
        # como recibo la informacion de la playlist que elegí, necesito id
        # playlist_id = dame_id_playlist(spotify, token_yutub, user_id_spotifai, nombre, 'spotify')
    elif opcion2 == 2:
        # uso una de las de ahí
        lista_spotifai: list = []
        print_playlists_de_user(usuario_actual, "spotify")
        seleccionar_playlist(usuario_actual, playlist_spotifai, "spotify", True)
        # recibo la informacion de la lista elegida
        importar_playlist(spotify, token_yutub,playlist_spotifai['id'], playlist_spotifai['name'],
                          "spotify", detalles_spotifai)
        # busco las canciones que están en spotify
        lista_canciones(detalles_spotifai, lista_spotifai, "spotify")
        playlist_id = detalles_spotifai['id']
    #comparo ambas listas
    lista_agregar: list = comparacion(lista_yutub, lista_spotifai, "youtube")
    uris: list = []
    lista_no_agregado: list = []
    # lista_encontrados: list = []
    # uris de las canciones
    for i in range(len(lista_agregar)):
        search = buscar_item(spotify, token_yutub, "spotify",
                             f"{lista_agregar[i][0]}, {lista_agregar[i][1]}", 1, ('track',))

        # acá voy agregando las uris de lo que encuentro
        comparacion_con_search_spotify(search, lista_agregar[i][0], lista_agregar[i][1], uris,
                                       lista_no_agregado)

    try:
        # esto es por si no hay uris, puede ser que no se encuentre nada
        agregar_cancion_a_spotify(playlist_id, uris, spotify)
    except tk.BadRequest:
        print("Upsi! Ninguna canción de las que estaban en su lista fueron encontradas en Spotify")

    if not emergencia:
        no_se_pudo: dict = {}
        no_se_pudo['no se pudo'] = lista_no_agregado
        return no_se_pudo
    else:
        playlist_emerg: dict = {}
        if opcion2 == 2:
            playlist_emerg = {
                'id': playlist_id,
                'servidor': 'spotify',
                'name': detalles_spotifai['name']
            }
        else:
            playlist_emerg = {
                'id': playlist_id,
                'servidor': 'spotify',
                'name': nombre
            }
        return playlist_emerg

### ----------------------- WORDCLOUD -------------------------------------------------------------
###################################################################################################

def wordcloud(usuario_actual: dict, spotify: object, youtube: object) -> None:
    servidor, datos_playlists = playlist_segun_servidor(usuario_actual, False)
    if datos_playlists:
        # acá se guarda la información de la playlist que elijo
        indice_playlist_elegida: int = seleccionar_playlist(usuario_actual, datos_playlists, servidor)

        if servidor == "youtube": 
            print("Puede ser que este resultado sea bastate malo, le recomiendo pasar la lista a spotify para un"
                  "mejor rendimiento :)")

        playlist_elegida: dict = datos_playlists[indice_playlist_elegida]

        if playlist_elegida["cant_tracks"] == 0:
            print("La playlist elegida esta vacia, no pudimos ni realizar el analisis.")
            input("Presione Enter para volver al menu principal: ")
        else:
            if servidor == "spotify":
                tracks_playlist: list = tracks_playlist_spotify(spotify, playlist_elegida["id"])
            else:
                tracks_playlist: list = tracks_playlist_youtube(youtube, playlist_elegida["id"])
            letra_total: str = ""
            # realmente toma mucho tiempo si es larga la playlist
            print("Esto va a tomar un tiempo, por favor imagine musica de ascensor\n"
                "tu tuutututut tuut utututu")
            letra_total = rejunte_letras(tracks_playlist, playlist_elegida, servidor)
            try:
                al_wordcloud(letra_total, usuario_actual['username'], playlist_elegida['id'])
                mostrame_esta_imagen(usuario_actual['username'], playlist_elegida['id'])
            except TimeoutError:
                # esto se arreglará para la reentrega
                print("Ouh no! Hubo un error y se supero el tiempo de espera, sepa disculpar")
    else:
        print(" Sin playlists no podemos crear la nube de palabras.")
        input("Presione Enter volver al menu principal: ")


def al_wordcloud(letra_total: str, usuario: str, id_playlist: str) -> None:
    # para que el request de algun valor como las letras de la canción es muy larga se debió hacer un json con todo el rejunte
    # el problema acá es que json no le cae muy bien el español u otros idiomas que no sean el ingles
    jsonito = json.dumps(letra_total)
    resp = requests.post('https://quickchart.io/wordcloud', json={
        "format": "png",
        "width": 1000,
        "height": 1000,
        "fontFamily": "serif",
        "fontScale": 15,
        "scale": "linear",
        "maxNumWords": 10,
        'minWordLength': 4,
        "removeStopwords": True,
        "text": jsonito,
            })

    with open(f'wordcloud_{usuario}_{id_playlist}.png', 'wb') as f:
        f.write(resp.content)


def mostrame_esta_imagen(usuario: str, id_playlist: str) -> None:
    # simplemente plotea la imagen
    img = cv.imread(f'wordcloud_{usuario}_{id_playlist}.png')
    cv.imwrite(f'wordcloud_{usuario}_{id_playlist}.jpg', img, [int(cv.IMWRITE_JPEG_QUALITY), 100])
    plt.imshow(img)
    plt.show()

### ----------------------- CREAR PLAYLISTS -------------------------------------------------------
###################################################################################################

def crear_playlist_spotify(usuario_actual: dict) -> tuple:
    # acá se crean las listas y devuelve el nombre que se le dio para buscar más tarde el id
    nombre: str = input("Indique el nombre para la playlist de Spotify: ")
    publica: str = input("Indique si desea que sea publica (s/n): ")
    if publica in "sS":
        public: bool = True
    else:
        public: bool = False
    descripcion: str = input("Indique una descripción: ")
    datos_playlist = usuario_actual["spotify"].playlist_create(usuario_actual["id_usuario_spotify"], nombre, public, descripcion)       # ES MUY LARGO
    print(vis.PLAYLIST_CREADA)
    return nombre, datos_playlist.id


def crear_playlist_youtube(youtube: object) -> tuple:
    # acá lo mismo pero para youtube
    nombre: str = input("Indicame el nombre bebe: ")
    descripcion: str = input("La descripcion please: ")
    eleccion_privacidad: str = perf.input_con_control(["p", "n"], "Privado (p) o No privado (n), esa es la cuestion: ",
                                                      2, "Mire que no tenemos todo el dia.")
    if eleccion_privacidad == "p":
        privaciti: str = 'private'
    else:
        privaciti: str = 'public'
    nueva_playlist: dict = youtube.playlists().insert(
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
    print(vis.PLAYLIST_CREADA)
    return nombre, nueva_playlist["id"]


def crear_playlist(usuario_actual: dict, token_youtube: object) -> None:
    # la función en si para que el usuario elija en que plataforma crearlo
    vis.youtube_spotify()
    opcion: int = input_num_con_control(1, 3)
    if opcion == 1:
        crear_playlist_youtube(token_youtube)
    elif opcion == 2:
        crear_playlist_spotify(usuario_actual)
    else:
        print(" Volviendo al menu...")
        
### ----------------------------- ANALISIS DE PLAYLISTS -------------------------------------------
###################################################################################################

### Funciones reutilizables >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def generar_playlist_de_user(usuario_actual: dict, servidor: str) -> list:
    """
    Pre: Recibe la informacion del usuario y el nombre del servidor elegido.
    Post: Devuelve una lista con las playlist (si es que las hay) del servidor pasado por parametro.
    """
    if servidor == "spotify":
        datos_playlists: list = datos_playlists_SP(usuario_actual["spotify"], usuario_actual["id_usuario_spotify"])
    else:
        datos_playlists: list = datos_playlists_YT(usuario_actual["youtube"])    
    return datos_playlists


def print_playlists_de_user(servidor: str, datos_playlists: list) -> None:
    #Recibe la informacion un servidor y una lista con las playlists del usuario.
    #Muestra por pantalla una lista con las playlists recibidas (si es que las hay).
    if len(datos_playlists) == 0:
        vis.no_playlist(servidor)
    elif datos_playlists and datos_playlists[0] == "SIN INTERNET":
        print("Necesitamos internet para esto, intentalo despues.")
    else:
        nombres_playlists = [playlist["nombre"] for playlist in datos_playlists]
        vis.visual_lista_elementos(nombres_playlists, f"Playlists de {servidor}", True)
    
def seleccion_servidor() -> str:
    #Devuelve un str del servidor elegido por el user entre las opciones disponibles
    servidor: str = input("Ingrese el servidor en el que desea buscar: ").lower()
    while not servidor == "spotify" and not servidor == "youtube":
        servidor: str = input("Servidor inválido, vuelva a ingresar >>> ").lower()
    return servidor

def playlist_segun_servidor(usuario_actual: dict, elegir_ambas: bool = True) -> tuple:
    #Recibe la información de usuario
    #Devuelve el nombre del servidor en el que elige trabajar el usuario
    vis.youtube_spotify(mostar_ambas=True)
    seleccion: int = input_num_con_control(1,3)
    print("Obteniendo datos...")
    if seleccion == 1:
        datos_playlists: list = generar_playlist_de_user(usuario_actual, "youtube")
        print_playlists_de_user("youtube", datos_playlists)
        servidor: str = "youtube"
    elif seleccion == 2:
        datos_playlists: list = generar_playlist_de_user(usuario_actual, "spotify")
        print_playlists_de_user("spotify", datos_playlists)
        servidor: str = "spotify"
    else:
        datos_playlists: list = []
        datos_playlists_YT: list = generar_playlist_de_user(usuario_actual, "youtube")
        datos_playlists_SP: list = generar_playlist_de_user(usuario_actual, "spotify")
        print_playlists_de_user("youtube", datos_playlists_YT)
        print_playlists_de_user("spotify", datos_playlists_SP)
        servidor: str = "unknown"

    if not elegir_ambas and seleccion == 3:
        servidor: str = seleccion_servidor()
        if servidor == "spotify":
            datos_playlists: list = datos_playlists_SP
        else:
            datos_playlists: list = datos_playlists_YT

    return servidor, datos_playlists


def comprobar_permisos(usuario_actual: dict, servidor:str, seleccion:int, datos_playlists: list) -> bool:
    #Recibe la información de usuario y el indice de playlist elegido
    #Devuelve si esta permitido hacer cambios en la playlist
    #Será true si es colaborativa o propiedad del usuario
    permitido: bool = False
    if servidor == "spotify":
        if datos_playlists[seleccion - 1]['collaborative']:
            permitido: bool = True
        else:
            dueño_playlist = datos_playlists[seleccion - 1]['dueño']
            if dueño_playlist["id"] == usuario_actual['id_usuario_spotify']:
                permitido: bool = True
    return permitido

def seleccionar_playlist(usuario_actual, datos_playlists: list, servidor: str, permisos: bool = False) -> int:
    permitido: bool = False
    print("Seleccione una playlist ")
    seleccion: int = input_num_con_control(1, len(datos_playlists))
    permitido: bool = comprobar_permisos(usuario_actual, servidor, seleccion, datos_playlists)
    while servidor == "spotify" and permisos and not permitido:
        print("No puede modificar esa playlist. Elija una suya o que sea colaborativa.")
        seleccion = input_num_con_control(1, len(datos_playlists))
        permitido = comprobar_permisos(usuario_actual, servidor, seleccion, datos_playlists)    
    return seleccion-1

def tracks_playlist_spotify(spotify: object, id_playlist_elegida: str) -> list:   # Revisar typing
    datos_buscados: str = "items(track(artists(name), id, name, track_number, uri))"
    datos_tracks_desordenado: dict = spotify.playlist_items(id_playlist_elegida, datos_buscados, as_tracks=True)
    datos_tracks: list = []
    if datos_tracks_desordenado["items"]:
        for dato in datos_tracks_desordenado["items"]:
            datos_track: dict = {}
            datos_track["nombre"] = dato["track"]["name"]
            datos_track["id"] = dato["track"]["id"]
            artistas: list = []
            for artista in dato["track"]["artists"]:
                artistas.append(artista["name"])
            datos_track["artistas"] = artistas
            datos_track["numero_track"] = dato["track"]["track_number"]
            datos_track["uri"] = dato["track"]["uri"]
            datos_tracks.append(datos_track)
    return datos_tracks

def normalizar_playlist_spotify(info_playlist:list, detalles:dict,
                                playlist_id:str, playlist_nombre:str) -> None:
    #Recibe los datos dados por la api en list info_playlist
    #Devuelve los datos con las keys asignadas en dict detalles
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

def normalizar_tracks_youtube(datos_desordenados: dict) -> list:
    datos_tracks: list = []
    for dato in datos_desordenados:
        datos_tracks.append(
                {'nombre': dato['snippet']['title'],
                 'id': dato['id'],
                 'artistas': dato['snippet']['videoOwnerChannelTitle'],
                 'numero_track': dato['snippet']['position'],
                 'uri': 'desconocido'
                 }
        )
    return datos_tracks


def tracks_playlist_youtube(youtube: object, id_playlist_elegida: str) -> list:   # Revisar typing
    datos_tracks: list = []
    response = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=id_playlist_elegida,
                    maxResults="50"
                    ).execute()

    nextPageToken = response.get("nextPageToken")
    while ("nextPageToken" in response):
        nextPage = youtube.playlistItems().list(
                        part="snippet",
                        playlistId=id_playlist_elegida,
                        maxResults="50",
                        pageToken=nextPageToken
                        ).execute()
        response["items"] = response["items"] + nextPage["items"]

        if "nextPageToken" not in nextPage:
            response.pop("nextPageToken", None)
        else:
            nextPageToken = nextPage["nextPageToken"]
    datos_tracks: list = normalizar_tracks_youtube(response['items'])
    return datos_tracks


def normalizar_playlist_youtube(info_playlist:list, detalles:dict, playlist_id:str, playlist_nombre:str) -> None:
    #Recibe los datos dados por la api en list info_playlist
    #Devuelve los datos con las keys asignadas en dict detalles
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
    #Recibe una playlist (nombre, id, servidor) y los objetos de los servidores disponibles
    #La devuelve con todos sus items detallados
    info_playlist:list=list()
    if servidor == "spotify":
        info_playlist.append(Spotify.playlist(spotify, playlist_id, fields=None, market=None, as_tracks=True))
        normalizar_playlist_spotify(info_playlist, detalles_playlist, playlist_id, playlist_nombre)
    elif servidor == "youtube":
        youtube: object = token_youtube
        response = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults="50"
                    ).execute()

        nextPageToken = response.get("nextPageToken")
        while ("nextPageToken" in response):
            nextPage = youtube.playlistItems().list(
                            part="snippet",
                            playlistId=playlist_id,
                            maxResults="50",
                            pageToken=nextPageToken
                            ).execute()
            response["items"] = response["items"] + nextPage["items"]

            if "nextPageToken" not in nextPage:
                response.pop("nextPageToken", None)
            else:
                nextPageToken = nextPage["nextPageToken"]
        
        for item in response['items']: #lista de dicts
            info_playlist.append(item)
        normalizar_playlist_youtube(info_playlist, detalles_playlist, playlist_id, playlist_nombre)


def exportar_dict_a_csv(extension:str, usuario:str, mi_dict:dict, nombre:str) -> None:
    # Funciona para un solo dict, no nested dicts, y reescribe el archivo
    #Recibe un dict, lo guarda como archivo csv
    with open(f"analisis_{nombre}_de_{usuario}.{extension}", "w") as archivito:
        w = csv.DictWriter(archivito, mi_dict.keys())
        w.writeheader()
        w.writerow(mi_dict)
    # else:
    #     with open(f"analisis_playlists_de_{usuario}.{extension}", "a") as archivito:
    #         w = csv.DictWriter(archivito, mi_dict.keys())
    #         w.writerow(mi_dict)


### Funciones propias del analisis de atributos >>>>>>>>>>>>>>>>>>>>>>>>

def analisis_de_playlist(usuario_actual: dict) -> None:
    #Recibe los datos del usuario y selecciona una playlist de una lista para analizar
    #Llama a las funciones necesarias para el analisis
    servidor, datos_playlists = playlist_segun_servidor(usuario_actual, False)
    if not datos_playlists:
        print(f" Sin playlists no podemos realizar ningun analisis.")
        input("Presione Enter volver al menu principal: ")
    else:
        indice_playlist_elegida: int = seleccionar_playlist(usuario_actual, datos_playlists, servidor)
        if datos_playlists[indice_playlist_elegida]["cant_tracks"] == 0:
            print("La playlist elegida esta vacia, no pudimos realizar un analisis.")
            input("Presione Enter para volver al menu principal: ")
        else:
            realizar_analisis_playlist(usuario_actual, datos_playlists[indice_playlist_elegida], servidor)

def analizar_track(track: dict, atributos_track: dict, spotify: object, atributos: list, servidor: str = 'spotify') -> None:
    # Recibe un dict con un track de Spotify
    # Le agrega a atributos_track los atributos de cada track
    if servidor == "spotify":
        print(f"Analizando track {track['nombre']}...\n")
        analisis = spotify.track_audio_features(track['id'])

        for atrib in atributos:
            atributos_track[atrib] = getattr(analisis, atrib)

def realizar_analisis_playlist (usuario_actual: dict, playlist_elegida: dict, servidor: str) -> None:
    #Recibe datos de usuario y de la playlist a analizar atributos
    #Guarda un csv con los atributos promediados
    atributos_playlist: dict = {}
    atributos_track: dict = {}
    fecha = date.today()

    atributos: list = [
        'acousticness', 'danceability', 'energy', 'liveness', 'loudness',
        'valence', 'tempo', 'duration_ms', 'instrumentalness', 'speechiness'
    ]

    if servidor == "spotify":
        tracks_spotify: list = tracks_playlist_spotify(usuario_actual["spotify"], playlist_elegida["id"])
        for track in tracks_spotify:
            try:
                analizar_track(track, atributos_track, usuario_actual['spotify'], atributos)
                for key,value in atributos_track.items():
                    if atributos_playlist == {} and key not in atributos_playlist.keys():
                        atributos_playlist['fecha de analisis'] = fecha
                        atributos_playlist['id'] = playlist_elegida["id"]
                        atributos_playlist['playlist name'] = playlist_elegida["id"].encode()
                        atributos_playlist[key] = value
                    elif key not in atributos_playlist.keys():
                        atributos_playlist[key] = value
                    else:
                        atributos_playlist[key] += value
                exportar_dict_a_csv('csv', usuario_actual['username'], atributos_playlist,
                                    playlist_elegida['id'])
            except TimeoutError:
                print(vis.NO_INTERNET)

        if os.path.isfile(f"analisis_{playlist_elegida['id']}_de_{usuario_actual['username']}.csv"):
            print(f"Se ha creado un archivo con los atributos de la playlist {atributos_playlist['playlist name']} \n"
                  f"en el directorio {os.getcwd()}")
        else:
            print("Ha habido un error al generar el archivo. Intentelo nuevamente.")

    else:
        print("No podemos realizar un analisis de atributos musicales para"
              " playlists en youtube.") #Youtube Music API when ??
        print("Podemos sincronizar con spotify y realizar el analisis de las canciones que estén en esa plataforma.")
        sincronizar:str = input("[S] aceptar \nCualquier [Tecla] volver\n     >>>   ").lower()
        if sincronizar == "s":
            sincronizacion_de_emergencia(usuario_actual, playlist_elegida)


def sincronizacion_de_emergencia(usuario_actual:dict, mi_playlist:dict) -> None:
    #recibe una playlist de youtube (dict mi_playlist)
    #la sincroniza con spotify para realizar el analisis de los atributos de los tracks
    temp_spotify: dict = dict()
    detalles_spotify: dict = dict()
    detalles_youtube: dict = dict()
    nueva_playlist:dict = sincronizacion_youtube_a_spotify(usuario_actual, temp_spotify, detalles_spotify,
                                     usuario_actual['youtube'], usuario_actual['id_usuario_youtube'],
                                     mi_playlist, detalles_youtube, usuario_actual['spotify'], True)
    realizar_analisis_playlist(usuario_actual, nueva_playlist)

### ------------------------ BÚSQUEDA DE CANCIONES ------------------------------------------------
###################################################################################################

def buscar_cancion(spotify: object, token_youtube: str, resultados: list, servidor:str) -> None:
    # Recibe objetos de los servidores, resultados como lista vacia y el servidor elegido
    # Devuelve resultados con los datos de resultados de busqueda ya ordenados

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


def buscar_item(spotify:object, token_youtube:object, servidor:str, query:str, limit:int, types:tuple=('track',))-> tuple:
    #Recibe objetos de las app, los datos de busqueda como query, maximo de resultados como limit
    #Devuelve search con los resultados de la busqueda en la api
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

def agregar_cancion_a_youtube(playlist_id: str, cancion_id: str, youtube: object) -> None:
    #Agrega una canción a youtube
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


def agregar_a_playlist(usuario_actual:dict, cancion: dict, servidor:str, playlist: dict) -> None:
    #Agrega una canción a una playlist
    if servidor == 'spotify':
        agregar_cancion_a_spotify(playlist['id'], [cancion['uri']], usuario_actual['spotify'])
    elif servidor == 'youtube':
        agregar_cancion_a_youtube(playlist['id'], cancion['id'], usuario_actual['youtube'])


def agregar_cancion_a_spotify(playlist_id:str, uri_cancion:list, spotify:object) -> None:
    #Agrega canciones a spotify (acepta multiples canciones)
    #uri_cancion recibe una lista de hasta 100 uris
    try:
        spotify.playlist_add(playlist_id, uri_cancion)
        print("Canción agregada correctamente")
    except TimeoutError:
        print(vis.NO_INTERNET)


def info_html_de_youtube(cancion:dict) -> None:
    #recibe informacion de cancion en youtube en dict
    #devuelve track y artista del html usando libreria youtube_dl
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
    # Recibe dict de canción y servidor
    # Muestra el nombre, artista y la letra de la canción
    nombre = cancion['name']
    artistas: str = ','.join(cancion['artists'])

    vis.mostrar_cancion(cancion, seleccion)
    token_genius: str = perf.sacar_info_json("credenciales.json")["genius"]["token_genius"]
    letra: str = extraer_letra(token_genius, nombre, artistas)
    if letra == "":
        print("No se ha encontrado ninguna letra para esta canción.")
        print("\n- [x] Si quiere buscar la letra por otros medios"
              "\n- Cualquier [Tecla] para finalizar")
    else:
        print(letra)
        print("\n- [x] Si la letra mostrada es incorrecta y quiere "
                        "volver a buscarla\n- Cualquier [Tecla] para finalizar")

    es_la_letra = input("     >>>   ").lower()
    if es_la_letra == "x":
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


def administracion_de_canciones(usuario_actual: dict) -> None:
    #Recibe datos de usuario
    #Mediante funciones auxiliares, busca canción en servidores
    #Ofrece visualizarla o agregarla a playlist
    resultados: list = list()
    titulo: str = "Administrar canción"
    opciones: list = [
        "Visualizar", "Agregar a playlist"
    ]

    servidor: str = seleccion_servidor()
    buscar_cancion(usuario_actual['spotify'], usuario_actual['youtube'], resultados, servidor)
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
            playlists: list = generar_playlist_de_user(usuario_actual, servidor)
            if playlists:
                print_playlists_de_user(servidor, playlists)
                print("Seleccione una playlist ")
                indice_playlist_elegida: int = input_num_con_control(1, len(playlists))
                playlist_elegida: dict = playlists[indice_playlist_elegida-1]
                agregar_a_playlist(usuario_actual, resultados[seleccion_cancion-1], servidor, playlist_elegida)
            else:
                print("Ups, no hay playlist") # Aqui para que vaya a agregar playlists.
    else:
        print("No hemos obtenido ningún resultado de la búsqueda")

###------------------------- MANEJO DE LYRICS ------------------------------------------------------
####################################################################################################

def extraer_letra(token_genius, cancion: str = "0", artista: str = "0") -> str:
    # Recibe token de genius y datos de cancion (nombre y artista)
    # Devuelve la letra, si no la encuentra devuelve str = ""
    # Si no recibe nombre ni artista, el usuario los ingresa manualmente
    ser_o_no_ser: str = "aun no paso nada"
    genius = Genius(token_genius)
    # saca los headers
    genius.remove_section_headers = True
    # Excluye canciones que tengan esos nombres
    genius.excluded_terms = ["(Remix)", "(Live)", "(Cover)"]
    # Saca mensajes sobre el estatus de la canción
    genius.verbose = False

    if cancion == "0" and artista == "0":
        #Si queremos que el usuario busque el nombre de la canción manualmente
        es_cancion: bool = False
        while es_cancion == False:
            cancion = input("Nombre del cantante: ")
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


def rejunte_letras(tracks: list, playlist: dict, servidor: str) -> str:
    total_letrasas: str = ""
    # se recibe el token
    token_genius: str = perf.sacar_info_json("credenciales.json")["genius"]["token_genius"]
    if servidor == "spotify":
        # se busca las canciones de spotify directamente
        for cancioncita in tracks:
            letra: str = extraer_letra(token_genius, cancioncita['nombre'], cancioncita["artistas"][0])     # Que pasa con los otros artistas?
            # se suman
            total_letrasas = total_letrasas + letra
    elif servidor == "youtube":
        for cancioncita in tracks:
            # aca hay que hacer una limpieza porque sino no da nada
            cancion, artista = limpieza(cancioncita["nombre"], cancioncita["artistas"])
            letra: str = extraer_letra(token_genius, cancion, artista)
            total_letrasas = total_letrasas + letra
    return total_letrasas

###------------------------- LISTADO DE PLAYLISTS  -------------------------------------------------
####################################################################################################

def playlists_spotify(spotify, id_usuario) -> None:
    """ Recupera la información de las playlists de Spotify de un usuario """
    datos_playlists = spotify.playlists(id_usuario, 50)
    nombres = [x.name for x in datos_playlists.items]
    if nombres:
        vis.visual_lista_elementos(nombres, "Playlists de Spotify", True)
    else:
        vis.no_playlist("spotify")


#### ----------------------------- AGREGAR DATOS DE SPOTIFY AL PERFIL -----------------------------
###################################################################################################

def obtener_credYT(nombre: str) -> dict:
    """ Devuelve las credenciales del nombre indicado. En caso de no encontrarlas, devuelve un 
    diccionario vacío"""
    credenciales: dict = {}
    if os.path.isfile("datos_perfiles.json"):
        datos: dict = perf.sacar_info_json("datos_perfiles.json")
        credenciales: dict = datos[nombre]["youtube"]
    return credenciales

#### ----------------------------- AUTENTICACIÓN YOUTUBE ------------------------------------------
###################################################################################################

def id_canal_youtube(youtube:object) -> None:
    """ Retorna el identificador de un canal de Youtube (ID) """
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
    if os.path.isfile("credenciales.json"):
        vis.inicio()
        usuario_actual: dict = {"username": ""}
        perf.manejo_perfiles(usuario_actual)
        terminar: bool = True
        if perf.datos_agregados_correctamente(usuario_actual):
            terminar: bool = False
        """
        datos_SP = datos_playlists_SP(usuario_actual["spotify"], usuario_actual["id_usuario_spotify"])
        print(datos_SP)
        datos_YT = datos_playlists_YT(usuario_actual["youtube"])
        print(datos_YT)
        """
        while not terminar:
            print(vis.MENU)
            seleccion: int = input_num_con_control(0, 7)
            if seleccion == 1:
                #Listar las playlist
                playlist_segun_servidor(usuario_actual)
                input(" Presione Enter para volver al menu principal: ")
            elif seleccion == 2:
                #Exportar analisis de playlist a CSV
                analisis_de_playlist(usuario_actual)
            elif seleccion == 3:
                # Crear playlist
                crear_playlist(usuario_actual, usuario_actual['youtube'])
            elif seleccion == 4:
                #Buscar y administrar canción
                administracion_de_canciones(usuario_actual)
            elif seleccion == 5:
                #Sincronizar playlists
                spotify_vs_youtube(usuario_actual, usuario_actual['spotify'], usuario_actual['youtube'],
                                usuario_actual['id_usuario_spotify'], usuario_actual['id_usuario_youtube'])
            elif seleccion == 6:
                #Generar wordcloud
                wordcloud(usuario_actual, usuario_actual['spotify'], usuario_actual['youtube'])
            elif seleccion == 7:
                #Cambiar de perfil
                perf.manejo_perfiles(usuario_actual)
                if "spotify" not in usuario_actual:    # Si no esta entonces el usuario cambio.
                    if not perf.datos_agregados_correctamente(usuario_actual):
                        terminar: bool = True
            else:
                terminar: bool = True
    else:
        vis.falta_archivo()
    
main()
