
import tekore as tk
import requests

def main() -> None:
    id_cliente: str = "176365611325455e8059fbd545371d89"
    usuario: str = "3165tas3s4za67w2jmbzq4kgr2b4"
    key_secreta: str = "ed35a90b681042f4bbad9f284383c88a"
    url_autenticacion: str = "https://accounts.spotify.com/authorize/"
    uri_redireccion: str = "https://open.spotify.com/"

    autorizacion: int = (requests.get(url_autenticacion, {
            "client_id": id_cliente,
            "response_type": "code",
            "redirect_uri": uri_redireccion
            }
        )).status_code
    
    if (autorizacion == 200): # Si obtengo el código 200 es porque está todo OK.

        # Genero un token para intercambiar en la autenticación de acceso.
        token: tk.Token = tk.request_client_token(id_cliente, key_secreta)
        
        spotify: object = tk.Spotify(token)

        # Consumo un servicio.
        item: object = spotify.playlist("0VRmNHCCKwXtLG9gvzg2uk?si=54ed5ae222c1459c").tracks.items[0].track
        # Formateo e imprimo por pantalla.
        cancion: str = item.name
        interprete: str = item.artists[0].name
        print(cancion, "-", interprete)

main()

