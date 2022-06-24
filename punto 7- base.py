import matplotlib.pyplot as plt
import cv2 as cv
import requests
from lyricsgenius import Genius


def ingreso_genius()->str:
    client_id: str = "LkrBCrYXlZO4Wm7Hx1X-AU0g9z_bNYc2ehowpFLNhgcVa-MdX8J1zceedRf59FNN"
    client_secret: str = "nRzbwpwEiEcic8uN9qyXRKAwo8O2e48lstan5rtc8F8FKIw6QbY1DUGV8P_FTzom763BRHuJWKcowt7jm9U8mQ"
    token_genius: str = "OomA5Dwkt15uqiCNHKthDcDx7gqYbFAkXeQFoX_DHqu-C6NQzyuBoxOY5o76C64P"
    return token_genius




def extraer_letra(token_genius, cancion: str = "0", artista: str = "0") -> str:
    genius = Genius(token_genius)
    es_cancion: bool = False
     # saca los headers
    genius.remove_section_headers = True
    # Exclude songs with these words in their title
    genius.excluded_terms = ["(Remix)", "(Live)", "(Cover)"]
    # Turn off status messages
    genius.verbose = False

    if cancion == "0" and artista == "0":
        es_cancion: bool = False
        while es_cancion == False:
            nombre_cancion = input("Nombre del cantante:")
            nombre_cantante = input("Nombre de canción: ")
            song = genius.search_song(nombre_cancion, nombre_cantante)
            print(song)
            ser_o_no_ser: str = input("Es la canción que usted busca? (s/n)")
            if ser_o_no_ser in "sS":
                es_cancion = True
            else:
                es_cancion = False
    else:
        song = genius.search_song(cancion, artista)
    letra_song: str = str(song.lyrics)
    return letra_song


def al_wordcloud(letra_total: str)->None:

    resp = requests.post('https://quickchart.io/wordcloud', json={
        'format': 'png',
        'width': 1000,
        'height': 1000,
        'fontScale': 15,
        'scale': 'linear',
        'maxNumWords': 10,
        'removeStopwords': True,
        'minWordLength': 4,
        'text': letra_total,
    })

    with open('newscloud.png', 'wb') as f:
        f.write(resp.content)




def rejunte_letras(detalles: dict)->str:
    token_genius = ingreso_genius()
    total_letrasas: str = ""
    for cancioncita in range(len(detalles['tracks']['items'])):
        letra: str = extraer_letra(token_genius,detalles['tracks']['items'][cancioncita]['name'],
                                   detalles['tracks']['items'][cancioncita]['artists'])
        total_letrasas = total_letrasas + letra
    return total_letrasas


def mostrame_esta()->None:
    img = cv.imread('newscloud.png')
    cv.imwrite('modified_img.jpg', img, [int(cv.IMWRITE_JPEG_QUALITY), 100])
    plt.imshow(img)
    plt.show()



def wordcloud() -> None:
    detalles: dict = {}
    # eleccion de lista
    # seleccionar_playlist()
    # normalizar_playlist()
    letra_total = rejunte_letras(detalles)
    al_wordcloud(letra_total)
    mostrame_esta()

def pruebiña()->None:
    token = ingreso_genius()
    letra = extraer_letra(token)
    al_wordcloud(letra)
    mostrame_esta()

def main():
    pruebiña()

main()
