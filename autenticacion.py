import tekore as tk
import requests

def main() -> None:
    id: str = "176365611325455e8059fbd545371d89"
    key_secreta: str = "ed35a90b681042f4bbad9f284383c88a"
    url_autenticacion: str = "https://accounts.spotify.com/authorize/"
    uri_redireccion: str = "https://open.spotify.com/"

    autorizacion: int = (requests.get(url_autenticacion, {
            "client_id": id,
            "response_type": "code",
            "redirect_uri": uri_redireccion
            }
        )).status_code
    print(autorizacion)
    

    """ ###usuario: str = "3165tas3s4za67w2jmbzq4kgr2b4"
    
    token_acceso: tk.Token = tk.request_client_token(cliente_id, cliente_secreta)
    print(token_acceso)

    ##url: str = "https://api.spotify.com/v1/users/" + usuario
    requests.post()
 """
main()

