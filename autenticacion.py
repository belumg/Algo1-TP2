import tekore as tk
import requests

def autenticar() -> str:
    """ Spotify """
    id_cliente: str = "176365611325455e8059fbd545371d89"
    usuario: str = "3165tas3s4za67w2jmbzq4kgr2b4"
    key_secreta: str = "ed35a90b681042f4bbad9f284383c88a"
    url_autorizacion: str = "https://accounts.spotify.com/authorize"
    url_autenticacion: str = "https://accounts.spotify.com/api/token"
    uri_redireccion: str = "https://open.spotify.com/"
    uri_solicitud: str = "https://api.spotify.com/v1/"

    autorizacion: object = (requests.get(url_autorizacion, {
            "client_id": id_cliente,
            "response_type": "code",
            "redirect_uri": uri_redireccion
            }
        ))

    if (autorizacion.status_code == 200): # Si obtengo el código 200 es porque está todo OK.
        
        # Genero un token de autenticación. Lo usaré cada vez que haga una petición.
        token_acceso: str = tk.request_client_token(id_cliente, key_secreta)

        """ # Hago una petición. Ej: deseo conocer todas las canciones de una playlist.
        resultado: object = requests.get(uri_solicitud+"playlists/"+"0VRmNHCCKwXtLG9gvzg2uk", headers={
            "Authorization": "Bearer {token}".format(token=token_acceso)}
            )
        print(resultado) """

    return token_acceso

print(autenticar())

