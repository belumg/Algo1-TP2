import webbrowser
import time

def autenticarYT(id_cliente: str, key_secreta: str) -> str:
    # Seteo las variables necesarias.
    url_autorizacion: str = "https://accounts.google.com/o/oauth2/auth?"
    scope: str = "https://www.googleapis.com/auth/youtube"

    print("Autorizar la aplicación y pegar enlace de redirección a continuación: ", end="")
    time.sleep(1.5)
    # Abro una ventana en el navegador para que el usuario autorice el uso de la aplicación.
    webbrowser.open(
        url_autorizacion+"client_id="+id_cliente+"&redirect_uri="+scope+"&scope="+scope+"&response_type=token"
        )
    url_respuesta: str = str(input())
    inicio: int = url_respuesta.find("access_token=")+13 #Sumo la longitud de la cadena "access_token="
    fin: int = url_respuesta.find("&token_type=")
    # Capturo el token.
    token: str = url_respuesta[inicio:fin]


    return token


print(autenticarYT("270225542083-vifnqbu0383uf3pv53d7pra1t3e847ko.apps.googleusercontent.com","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"))
