### -------------------- BÚSQUEDA DE CANCIONES ---------------------------------------
######################################################################################


def buscar_item(token:str, servidor:str, query:str, limit:int, types:tuple=('track',))-> None:
    #cambiando el tipo podemos buscar playlists, albums, artistas, etc
    if servidor == "spotify":
        spotify = tk.Spotify(token)
        search = Spotify.search(spotify, query, types=types, market=None, include_external=None, limit=limit, offset=0)
    else:
        #ver si youtube devuelve tupla y sino normalizar o hacer otra función
        pass
    return search


def mostrar_busqueda_canciones(resultados:list) -> None:
    # !!! to-do !!!
    # mover a vis y modificar acorde
    print("---Resultados de búsqueda---")
    for i in range(len(resultados)):
        print(f"*****Resultado {i + 1}*****")
        print(f"{resultados[i]['name']}")
        print(f"Artistas: {','.join(resultados[i]['artists'])}")
        print(f"Album: {resultados[i]['album']}\n")


def buscar_cancion(token_spotify:str, resultados:list) -> None:
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
    servidor=input("Ingrese el servidor en el que desea buscar: ").lower()
    while not servidor == "spotify" and not servidor == "youtube":
        servidor=input("Servidor inválido, vuelva a ingresar >>> ").lower()
    cancion= input("Ingrese el nombre de la canción a buscar >>> ")
    artista=input("Ingrese el artista >>> ")

    if servidor == "spotify":
        print("Buscando...")
        search= buscar_item(token_spotify, servidor, f"{cancion}, {artista}", 3, ('track','artist'))

        for x in search:
            for item in x.items:
                item_n:dict=dict()
                item_n['id'] = item.id
                item_n['name'] = item.name
                item_n['artists'] = []
                item_n['album']= item.album.name
                for artist in item.album.artists:  #artists es lista en model
                    item_n['artists'].append(artist.name)
                resultados.append(item_n)

    mostrar_busqueda_canciones(resultados)