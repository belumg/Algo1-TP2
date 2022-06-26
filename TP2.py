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
