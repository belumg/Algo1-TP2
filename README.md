# Trabajo Práctico Nº 2. (Versión 0.1.3006.)
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


## Bugs.

Los problemas están proyectados arreglarse en la versión 1.0.0
* Varias aplicaciones al requerir el uso de playlists de Youtube y de Spotify poseen un error al llamar a una lista ya creada pero de contenido nulo. Para evitar que el código “rompa” se procedió a ingresar un Try/Except.
* Se genera un error (aleatorio, solo con una cuenta de todas las que se usaron de prueba) al pedir los datos del usuario actual, según la documentación del tekore “el servidor entendió la solicitud, pero se niega a cumplirla.” 
* Si se crea una playlist en el transcurso del programa, el diccionario que contiene la información no lo recibe por lo que no aparece en las opciones. 
* El wordcloud no da buenos resultados para otro idioma que no sea en ingles, esto es debido a la implementación de json por la longitud de las listas. Se pensó en dos soluciones, utilizar una librería de wordcloud o realizar el conteo de cantidad de repeticiones de la letra a mano para solo mandarle las repetidas con la cantidad de veces que se repitio en un texto más pequeño.
* Sólo imprime 20 listas de spotify, si el usuario posee más no se podrán ver en pantalla.
