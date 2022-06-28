LONGITUD = 45

LOGO_INICIO: str = """
    ╔════════════════════════════════════════════════════════════╗
        ⠀⠀⠀⢲⣦⠀⢠⣶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⠀⠀⠀⠀⠀⠀⠀  ⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀  
        ⠀⠀⠀⠘⣿⡄⣼⡟⢀⣤⣤⣄⠀⢠⣄⠀⣠⡄⠀⠀⠀⠀      ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀      Este Software es traido a ustedes por:
        ⠀⠀⠀⠀⢹⣷⣿⠁⣿⡏⠙⣿⡆⢸⣿⠀⣿⡇⠀⠀⠀⠀      ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀          
        ⠀⠀⠀⠀⠈⣿⡏⠀⣿⡇⠀⣿⡇⢸⣿⠀⣿⡇⠀⠀⠀⠀      ⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀          - Ana Daniela Villalba
        ⠀⠀⠀⠀⠀⣿⡇⠀⢿⣧⣰⣿⠇⢸⣿⣤⣿⡇⠀⠀⠀⠀      ⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀          
        ⠀⠀⣀⣀⣀⣉⣁⣀⣀⣉⣉⣁⣀⣀⣉⣁⣈⣁⣀⣀⠀⠀     ⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄          - María Belén Guatto
        ⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶    ⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇          
        ⣿⣿⣿⣉⠉⠉⣉⣿⣿⣿⣿⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿    ⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃          - Camila Solari
        ⣿⣿⣿⣿⡇⢸⡟⠛⣿⠛⢻⠀⠘⠛⠻⡿⠛⡛⠻⣿⣿⣿      ⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀          
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


def menu_perfiles(perfil: str) -> None:
    """
    Pre: Recibe un string, si esta vacio entonces el usuario aun no eligio un perfil.
    Post: Imprime un menu con 3 opciones (perfil guardado, ingresar perfil, salir o volver al menu).
    """
    if not perfil:
        mensaje: str = "Terminar el programa."
        mensaje_perfil: str = "Aun no eligio un perfil"
    else:
        mensaje: str = "Ingresar al menu de perfil"
        mensaje_perfil: str = perfil

    print(f"""
                ██████████████████████████████
                █▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█▄─██─▄█
                ██─█▄█─███─▄█▀██─█▄▀─███─██─██
                ▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀
         ╔══════════════════════════════════════════╗

          [1] Seleccionar perfil guardado.                  Perfil actual:                   

          [2] Ingresar nuevo perfil.                        - {mensaje_perfil}
          
          [3] {mensaje}
         ╚══════════════════════════════════════════╝  
    """)


def youtube_spotify(crear_perfil: bool = False, opciones_elegidas: list = []) -> None:
    """
    Pre: Recibe un bool y una lista.
    Post: Imprime un menu que tiene 3 valores que variaran segun los datos recibidos por parametro.
          Si el bool es True entonces apareceran los mensajes relacionados con perfiles.
          Caso contrario solo sera un menu simple que te da la opcion de volver al menu original.
    """
    youtube: str = ""
    spotify: str = ""
    if crear_perfil and opciones_elegidas:
        mensaje: str = "Crear perfil"
        if 1 in opciones_elegidas: youtube: str = "--> Permisos aceptados"  # REVISAR (PONER UN MEJOR STRING)
        if 2 in opciones_elegidas: spotify: str = "--> Permisos aceptados"
    elif crear_perfil and not opciones_elegidas:
        mensaje: str = "No crear perfil"
    else:
        mensaje: str = "Volver al menu"

    print(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            Elegir plataforma:        
        [1] Youtube      {youtube}
        [2] Spotify      {spotify}
        [3] {mensaje}
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)


NOMBRE_NO_VALIDO: str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            [NOMBRE INCORRECTO]
      Posibles causas:
        - Esta vacio.
        - Ese nombre ya existe.
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

INSTRUCCIONES: str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
              [INSTRUCCIONES]
     - Log in (si es necesario).
     - Aceptar los permisos.
     - Copiar nueva URL.
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

ERROR_URL: str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
             [URL INCORRECTA]
      Posibles causas:
        - Mal ingreso de datos.
        - No acepto los permisos.
        - Copio mal la URL. 
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

DATOS_GUARDADOS: str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      [DATOS GUARDADOS EXITOSAMENTE]
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

NO_PERFILES: str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
              NO ENCONTRAMOS
          NINGUN PERFIL GUARDADO
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""


def visual_lista_elementos(lista_mostrar: list, mensaje: str, enumerar: bool) -> None:
    """
    Pre: Recibe una lista no vacia, un mensaje que sera el titulo del menu
         y un bool que nos dira si tenemos que enumerar los elementos o no.
    Post: Imprime los elementos de la lista en un menu que tiene el mensaje ingresado.
    """
    maxima_long = len(sorted(lista_mostrar, key=len, reverse=True)[0]) + 5
    if maxima_long<LONGITUD: maxima_long = LONGITUD
    print(f"┏━{'━' * maxima_long}━┓")
    print(f"{mensaje}".center(maxima_long))
    print(f"┣━{'━' * maxima_long}━┫\n")
    if enumerar:
        for numero, dato in enumerate(lista_mostrar, 1):
            print(f" [{numero}] {dato}\n")
    else:
        for dato in lista_mostrar:
            print(f" - {dato}\n")
    print(f"┗━{'━' * maxima_long}━┛")
    if not enumerar:
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

def mostrar_nombre_vid(cancion: dict, orden: int, titulo: str = "") -> None:
    print(f"""     {titulo}
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓

         Cod. {orden}
         {cancion['name']}
         Canal: {','.join(cancion['artists'])}

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


MENU: str = """
                ██████████████████████████████
                █▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█▄─██─▄█
                ██─█▄█─███─▄█▀██─█▄▀─███─██─██
                ▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀
         ╔══════════════════════════════════════════╗
          [1] Listar las playlist actuales
          [2] Exportar analisis de playlist a CSV
          [3] Crear nueva playlist
          [4] Buscar y administrar canciones
          [5] Sincronizar playlist 
          [6] Nube de palabras de playlist 
          [7] Cambiar de perfil
          [0] Salir
         ╚══════════════════════════════════════════╝  
    """
