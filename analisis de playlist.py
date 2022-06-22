### --------------------- ANALISIS DE PLAYLISTS ---------------------
#####################################################################

### Funciones reutilizables >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def print_playlists_nombres(lista_playlists:dict):
    # !!! to-do !!!
    # mover a vis y modificar acorde
    for i in range(len(lista_playlists['items'])):
        print(f"{i+1} - {lista_playlists['items'][i]['name']}")


def seleccionar_playlist(todas_playlists_usuario:dict, mi_playlist:dict) -> None:
    print_playlists_nombres(todas_playlists_usuario)
    print("Seleccione una playlist ")
    seleccion=int(input(">>> "))
    # cuando este la parte de youtube, el dict de todas las playlist debe aclarar de que servidor es cada una
    #en vez de spotify poner       todas_playlists_usuario['items'][seleccion-1]['servidor']     o algo similar
    mi_playlist['servidor'] = 'spotify'
    # asumimos que las playlists se muestran con un número (== index+1) que las representa al momento de printearlas
    mi_playlist['info']=todas_playlists_usuario['items'][seleccion-1]


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


def importar_playlist(token, playlist_id:str, servidor:str, info_playlist:dict, detalles_playlist:dict) -> None:

    if servidor == "spotify":
        spotify = tk.Spotify(token)
        info_playlist.update(Spotify.playlist(spotify, playlist_id, fields=None, market=None, as_tracks=True))
        normalizar_playlist(info_playlist, detalles_playlist)
    else:
        pass


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
        print(f"Analizando track {track['track']['name']}...\n")
        analisis = spotify.track_audio_features(track['track']['id'])

        for atrib in atributos:
            atributos_track[atrib] = getattr(analisis, atrib)


def analisis_de_playlist(token:str, todas_playlists_usuario: dict, usuario:str) -> None:
    fecha = date.today()
    mi_playlist:dict=dict()
    atributos_playlist:dict={}
    atributos_track: dict = {}
    info_playlist:dict= {}
    detalles_playlist: dict = dict()
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

    seleccionar_playlist(todas_playlists_usuario, mi_playlist)
    importar_playlist(token, mi_playlist['info']['id'], mi_playlist['servidor'], info_playlist, detalles_playlist)

    for track in detalles_playlist['tracks']['items']:
        analizar_track(track, atributos_track, token, atributos)
        for key,value in atributos_track.items():
            if atributos_playlist == {} and key not in atributos_playlist.keys():
                atributos_playlist['fecha de analisis'] = fecha
                atributos_playlist['id'] = mi_playlist['info']['id']
                atributos_playlist['playlist name'] = mi_playlist['info']['name']
                atributos_playlist[key] = value
            elif key not in atributos_playlist.keys():
                atributos_playlist[key] = value
            else:
                atributos_playlist[key] += value

    # !!! to-do !!!
    # mover a vis y modificar acorde
    for key,value in atributos_track.items():
        atributos_playlist[key] = value / len(detalles_playlist['tracks']['items'])
        print(f"* {key} : {value}")

    exportar_dict_a_archivo('cvs', usuario, atributos_playlist, f"atributos_playlist_{mi_playlist['info']['id']}")



