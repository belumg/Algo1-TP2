import tekore as tk
import requests

def main() -> None:
    


    ###usuario: str = "3165tas3s4za67w2jmbzq4kgr2b4"
    cliente_id: str = "176365611325455e8059fbd545371d89"
    cliente_secreta: str = "ed35a90b681042f4bbad9f284383c88a"
    uri_redireccion: str = "https://open.spotify.com/"
    token_acceso: tk.Token = tk.request_client_token(cliente_id, cliente_secreta)
    print(token_acceso)

    ##url: str = "https://api.spotify.com/v1/users/" + usuario

main()

