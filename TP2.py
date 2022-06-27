import TP2_VISUAL as vis
import PERFILES as per

def main() -> None:
    vis.inicio()
    perfil: dict = {"nombre": ""}
    per.manejo_perfiles(perfil)
    terminar: bool = True
    if per.datos_agregados_correctamente(perfil):
        terminar: bool = False
    print(perfil)

main()
