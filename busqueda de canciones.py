### -------------------- BÚSQUEDA DE CANCIONES ---------------------------------------
######################################################################################


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


def agregar_cancion_a_spotify(playlist_id:str, uri_cancion:list, token:str) -> None:
    spotify = tk.Spotify(token)
    agregando = spotify.playlist_add(playlist_id, uri_cancion, position=None)

    if agregando.status_code == 200:
        print("Canción agregada correctamente")
    else:
        print("Ha habido un error al agregar la canción, intentelo nuevamente.")
        
        
def buscar_cancion(token_spotify: str, token_youtube:str, resultados: list) -> None:
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
        for x in search: #tupla #object
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
    elif servidor =="youtube":
        print("Buscando en youtube...")
        print(search)
        for x in search['items']: #dict
            item_n: dict = dict()
            item_n['id'] = x['id']['videoId']
            item_n['name'] = x['snippet']['title']
            item_n['artists'] = [x['snippet']['channelTitle']]
            item_n['album'] = "  "
            resultados.append(item_n)
