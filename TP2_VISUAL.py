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

def menu_perfiles(perfil:list) -> None:
    """
    Pre: Recibe una lista, si esta vacia entonces el usuario aun no eligio un perfil.
    Post: Imprime un menu con 3 opciones (perfil guardado, ingresar perfil, salir o volver al menu).
    """
    if not perfil:
        mensaje: str = "Terminar el programa."
        mensaje_perfil: str = "Aun no eligio un perfil"
    else:
        mensaje: str = "Volver al menu principal"
        mensaje_perfil: str = perfil[0]

    print(f"""
                ██████████████████████████████
                █▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█▄─██─▄█
                ██─█▄█─███─▄█▀██─█▄▀─███─██─██
                ▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀

         ╔══════════════════════════════════════════╗
                                                            
          [1] Seleccionar perfil guardado.                  Perfil elegido:                   
                                                            
          [2] Ingresar perfil.                              - {mensaje_perfil}

          [3] {mensaje}

         ╚══════════════════════════════════════════╝  
    """)

def youtube_spotify() -> None:
    """Imprime un menu con 3 opciones (Youtube, Spotify, Volver al menu)."""
    print(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            Elegir plataforma:        

        [1] Youtube 

        [2] Spotify

        [3] Volver al menu

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)

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

NO_PERFILES:str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
              NO ENCONTRAMOS
          NINGUN PERFIL GUARDADO
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

ERROR_URL :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
             [URL INCORRECTA]

      Posibles causas:
        - Mal ingreso de datos.
        - No acepto los permisos.
        - Copio mal la URL. 

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

def menu_opciones():
    print("""
                ██████████████████████████████
                █▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█▄─██─▄█
                ██─█▄█─███─▄█▀██─█▄▀─███─██─██
                ▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀

         ╔══════════════════════════════════════════╗
          
          [1] Listar playlist

          [2] Exportar playlist (CSV)

          [3] Crear nueva playlist

          [4] Buscar canciones

          [5] Sincronizar playlist

          [6] Analizar playlist

          [7] Cambiar de perfil

          [8] Salir

         ╚══════════════════════════════════════════╝        
    """)

OPCION_NO_DISPONIBLE :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          [OPCION NO DISPONIBLE]

       Primero debes autenticar un 
       perfil en alguna plataforma

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

def visual_lista_elementos(lista_mostrar:list, mensaje:str, enumerar:bool) -> None:
    """
    Pre: Recibe una lista no vacia, un mensaje que sera el titulo del menu
         y un bool que nos dira si tenemos que enumerar los elementos o no.
    Post: Imprime los elementos de la lista en un menu que tiene el mensaje ingresado.
    """
    maxima_long = len(sorted(lista_mostrar, key=len, reverse=True)[0]) +5
    if maxima_long < LONGITUD: maxima_long = LONGITUD
    print(f"┏━{'━'*maxima_long}━┓")
    print(f"{mensaje}".center(maxima_long))
    print(f"┣━{'━'*maxima_long}━┫\n")
    if enumerar:
        for numero, dato in enumerate(lista_mostrar, 1):
            print(f" [{numero}] {dato}\n")
    else:
        for dato in lista_mostrar:
            print(f" - {dato}\n")
    print(f"┗━{'━'*maxima_long}━┛")
    if not enumerar:
        input(" Presione Enter para volver al menu: ")

NO_PLAYLIST :str = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓

        No se encontraron playlists   
         guardadas en esta cuenta.

    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
