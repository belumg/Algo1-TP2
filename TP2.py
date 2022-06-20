import tekore as tk
import requests
import visual as vis

ID_CLIENTE: str = "ea4916f2e2d144a992b0f2d7bed6c25d"
CLIENTE_SECRETO: str = "e8efcd9f5ed541bda3a3b1653e1fc5e4"
URI_REDIRECCION: str = "http://localhost:8888/callback"
SCOPE = tk.scope.every

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

def auntenticar_perfil(datos_importantes) -> None:
    vis.youtube_spotify()
    opcion :int = opciones([1, 2])
    if opcion == 1:
        pass
    else:
        auntenticar_spotify(datos_importantes)

def playlists_spotify(datos_importantes) -> None:
    headers = {
    'Authorization': 'Bearer {token}'.format(token=datos_importantes[1]),
    'Content-Type' : 'application/json'
    }
    playlist = (requests.get(url = "https://api.spotify.com/v1/me/playlists", headers=headers))
    playlist = playlist.json()
    nombres_playlist :list = [x["name"] for x in playlist["items"]]
    if nombres_playlist:
        vis.visual_nombres_playlists(nombres_playlist, "Spotify")
    else:
        print(vis.NO_PLAYLIST)
        input(" Presione Enter para volver al menu: ")

def playlists_actuales(datos_importantes):
    vis.youtube_spotify()
    opcion :int = opciones([1, 2])
    if opcion == 1:
        pass
    else:
        playlists_spotify(datos_importantes)

def main() -> None:
    vis.inicio()
    terminar :bool = False
    datos_importantes :list = ["", ""]
    while not terminar:
        print(vis.MENU)
        opcion :int = opciones(range(1,9))
        if opcion == 1:
            auntenticar_perfil(datos_importantes)
            print(datos_importantes[1])
        elif (opcion in range(2,8) and
             (not datos_importantes[0] and not datos_importantes[1])):
            print(vis.OPCION_NO_DISPONIBLE)
        elif opcion == 2:
            playlists_actuales(datos_importantes)
        elif opcion == 8:
            terminar :bool = True
            
main()
