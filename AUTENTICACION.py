import tekore as tk
from webbrowser import open as web_open
import TP2_VISUAL as vis

ID_CLIENTE: str = "176365611325455e8059fbd545371d89"
CLIENTE_SECRETO: str = "ed35a90b681042f4bbad9f284383c88a"
URI_REDIRECCION: str = "http://localhost:8888/callback"
SCOPE = tk.scope.every

def guardar_nuevo_perfil(refresh_token, nombre_perfil) -> None:
    datos_guardar: tuple = (ID_CLIENTE, CLIENTE_SECRETO, URI_REDIRECCION, refresh_token)
    tk.config_to_file("cuentas_spotify.txt", datos_guardar, nombre_perfil)

def nuevo_perfil_spotify(nombre_perfil) -> None:
    """Permite que el usuario inicie sesion y de permisos y luego guarda sus datos en un archivo."""
    credenciales: tk.RefreshingCredentials = tk.RefreshingCredentials(ID_CLIENTE, CLIENTE_SECRETO, URI_REDIRECCION)
    auth = tk.UserAuth(credenciales, SCOPE)
    print(vis.INSTRUCCIONES)
    input("Presione Enter para que se abra Spotify: ")
    web_open(auth.url)
    print()
    print("Aqui abajo debes ingresar la URL que copiaste:  ")
    url :str = input("--->  ").strip()
    token_usuario: tk.RefreshingToken = auth.request_token(url=url)
    refresh_token: str = token_usuario.refresh_token
    guardar_nuevo_perfil(refresh_token, nombre_perfil)
    print(vis.DATOS_GUARDADOS)
