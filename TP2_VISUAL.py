LONGITUD = 45

LOGO_INICIO :str = """
    ╔════════════════════════════════════════════════════════════╗
        ⠀⠀⠀⢲⣦⠀⢠⣶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀  
        ⠀⠀⠀⠘⣿⡄⣼⡟⢀⣤⣤⣄⠀⢠⣄⠀⣠⡄⠀⠀⠀⠀      ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀      Este Software es traido a ustedes por:
        ⠀⠀⠀⠀⢹⣷⣿⠁⣿⡏⠙⣿⡆⢸⣿⠀⣿⡇⠀⠀⠀⠀      ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀          
        ⠀⠀⠀⠀⠈⣿⡏⠀⣿⡇⠀⣿⡇⢸⣿⠀⣿⡇⠀⠀⠀⠀      ⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀          - Ana Daniela Villalba
        ⠀⠀⠀⠀⠀⣿⡇⠀⢿⣧⣰⣿⠇⢸⣿⣤⣿⡇⠀⠀⠀⠀      ⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀          
        ⠀⠀⣀⣀⣀⣉⣁⣀⣀⣉⣉⣁⣀⣀⣉⣁⣈⣁⣀⣀⠀⠀      ⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄          - María Belén Guatto
        ⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶      ⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇          
        ⣿⣿⣿⣉⠉⠉⣉⣿⣿⣿⣿⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿      ⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃          - Camila Solari
        ⣿⣿⣿⣿⡇⢸⡟⠛⣿⠛⢻⠀⠘⠛⠻⡿⠛⡛⠻⣿⣿⣿      ⠀⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀          
        ⣿⣿⣿⣿⡇⢸⡇⠀⣿⠀⢸⠀⢸⡇⠀⡇⠀⠿⠀⣿⣿⣿      ⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁           - Carla Mendoza Coronado
        ⣿⣿⣿⣿⡇⢸⡇⠀⣿⠀⢸⠀⢸⡇⠀⡇⠀⣶⠒⣿⣿⣿      ⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
        ⣿⣿⣿⣿⣧⣼⣷⣤⣴⣦⣾⣤⣶⣤⣼⣿⣦⣤⣴⣿⣿⣿      ⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀          Agradecimiento especial a: Guido Costa
        ⠙⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠋      ⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁
    ╚════════════════════════════════════════════════════════════╝
"""

def inicio() -> None:
    """Imprime el logo del software."""
    print(LOGO_INICIO)
    input("         Presione Enter para continuar: ")
    print()

MENU_PERFILES = """
                ██████████████████████████████
                █▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█▄─██─▄█
                ██─█▄█─███─▄█▀██─█▄▀─███─██─██
                ▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀

         ╔══════════════════════════════════════════╗

          [1] Seleccionar perfil guardado.

          [2] Ingresar perfil.

         ╚══════════════════════════════════════════╝
"""

INSTRUCCIONES :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
              [INSTRUCCIONES]

     - Logearse (si es necesario).
     - Aceptar los permisos.
     - Copiar nueva URL.

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""

DATOS_GUARDADOS :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      [DATOS GUARDADOS EXITOSAMENTE]
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

def youtube_spotify() -> None:
    """Imprime un menu con 2 opciones (Youtube, Spotify)."""
    print(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            Elegir plataforma:        

        [1] Youtube 

        [2] Spotify

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)

ERROR_URL :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
             [URL INCORRECTA]

      Posibles causas:
        - Mal ingreso de datos.
        - No acepto los permisos.
        - Copio mal la URL. 

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""


MENU :str = """
                ██████████████████████████████
                █▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█▄─██─▄█
                ██─█▄█─███─▄█▀██─█▄▀─███─██─██
                ▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀

         ╔══════════════════════════════════════════╗

          [1] Autenticar perfil en Youtube y Spotify

          [2] Listar las playlist actuales
          
          [3] Exportar playlist elegida a CSV

          [4] Crear nueva playlist

          [5] Buscar nuevos elementos para playlist

          [6] Sincronizar playlist elegida

          [7] Nube de palabras de playlist elegida

          [8] Salir

         ╚══════════════════════════════════════════╝  
"""

OPCION_NO_DISPONIBLE :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          [OPCION NO DISPONIBLE]

       Primero debes autenticar un 
       perfil en alguna plataforma

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

def visual_nombres_playlists(lista_playlists:list, plataforma:str) -> None:
    """
    Pre: Recibe una lista no vacia junto con el nombre de la plataforma.
    Post: Imprime los elementos de la lista en un menu que tiene el nombre ingresado.
    """
    maxima_long = len(sorted(lista_playlists, key=len, reverse=True)[0])
    if maxima_long < LONGITUD: maxima_long = LONGITUD
    print(f"┏━{'━'*maxima_long}━┓")
    print(f" Playlists de {plataforma}".center(maxima_long))
    print(f"┣━{'━'*maxima_long}━┫\n")
    for playlist in lista_playlists:
        print(f" - {playlist}\n")
    print(f"┗━{'━'*maxima_long}━┛")
    input(" Presione Enter para volver al menu: ")

NO_PLAYLIST :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓

        No se encontraron playlists   
         guardadas en esta cuenta.

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""


def mostrar_cancion(cancion: dict, orden: int, titulo: str = "") -> None:
    print(f"""     {titulo}
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓

         Cod. {orden}
         {cancion['name']}
         Artistas: {','.join(cancion['artists'])}
         Album: {cancion['album']}

        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
        """)


def menu_con_opciones_cortas(titulo: str, opciones: list) -> None:
    # sirve para cualquier menu de opciones, solo enviar titulo y lista de opciones
    print(f"""     {titulo}
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓

    """)
    for i in range(len(opciones)):
        print(f"     [{i + 1}]  {opciones[i]}")
    print(f"""

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)
