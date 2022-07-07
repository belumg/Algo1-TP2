# Trabajo Práctico Nº 2. (Versión 0.2)
En el programa realizado se trabajó con las APIs de Youtube y Spotify. Se pidió un programa que pudiera realizar varias funciones sobre dichas aplicaciones, trabajando sobre los datos, cambiando y añadiendo información que se verá reflejada tanto en Spotify como en Youtube.


### Alumnas:
* Ana Daniela Villalba
* Carla Mendoza Coronado
* Belen María Guatto
* Camila Abigail Solari


## Librerías utilizadas :
-Tekore https://tekore.readthedocs.io/en/stable/

-Youtube_dl  https://github.com/ytdl-org/youtube-dl

-Google-api-client (para youtube) https://developers.google.com/youtube/v3/docs

-google-auth-oauthlib https://pypi.org/project/google-auth-oauthlib/

-lyricsgenius https://lyricsgenius.readthedocs.io/en/master/index.html

-matplotlib https://matplotlib.org/

-QuickChart Word Cloud API https://quickchart.io/documentation/word-cloud-api/


## Otros modulos que será necesario importar:
-opencv-python 

-csv

-os

-request

-time

-datetime

-json


## Descripción de la Aplicación:

La aplicación consta de varios puntos.

El menú conduce a cada una de las funciones, además de la posibilidad de un manejo efectivo de varios usuarios en el programa.

Se inicia con la autenticación, proceso por el cual cedemos nuestros permisos para realizar cambios en ambas plataformas, generando un objeto de comunicación con la API. Gracias a este logramos obtener y devolver valores. 

Las siguientes funciones van desde el listado de las playlists hasta la posibilidad de pasar los datos de una plataforma a la otra. Estas dependen de la autenticación correcta y un ‘token’ valido.

Se pide pocas veces el ingreso de datos que no sean numericos para mayor comodidad del usuario, en su mayoría las acciones se expresan como menu de opciones.

## Requerimientos.

### Autenticación de Spotify:

-Presione Enter cuando se lo indique.

-Se abrirá automáticamente una pestaña en el navegador determinado.

-Por favor ingrese a su cuenta y acepte permisos.

-La ventana mostrará un mensaje de error, no se asuste, copie el url de la página.

-Proceda a pegar el url en el programa principal.

-Aparecerá un cartel con la validación de su autenticación.


### Autenticación de Youtube.

-Presione el link que le aparecerá en pantalla.

-Ingrese a su cuenta y acepte los permisos.

-Se le dará un código, cópielo.

-Proceda a pegar el código en el programa `principal.

-Aparecerá un cartel con la validación de su autenticación.

## Updates (07/07/2022)
* Credenciales_Genius, credenciales_SP, credenciales_YT unificados en Credenciales.json
* Eliminados los multiple return 
* Las playlists no están alojadas en el diccionario usuario_actual.
Se obtienen cada vez que se necesiten mostrar. De esta manera, 
la lista de playlists disponibles siempre estará actualizada aunque 
se realicen cambios en otros dispositivos.
* LISTAR PLAYLISTS contempla los casos donde no existen playlists en ese servidor
* Al intentar trabajar con playlists VACIAS, se emitirá un mensaje y no podrá procederse con la tarea.
* Mejoradas las excepciones, sobretodo para cuando no hay conexión a internet.
* Mejorado el funcionamiento de wordcloud.
* Spotify lista todas las playlists disponibles
