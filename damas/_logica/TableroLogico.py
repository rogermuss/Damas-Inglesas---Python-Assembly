from Estado import *
from Tipo import *
from Usuario import *
from Ficha import *
from Casilla import *


# Clase tablero
class TableroLogico:
    def __init__(self):
        self.matriz = [[Casilla(fila, col, None) for col in range(8)] for fila in range(8)]
        self.turno = True
        self.generar_casillas_con_fichas()

    def generar_casillas_con_fichas(self):
        for fila in range(8):
            for col in range(8):
                # Solo en casillas negras (por ejemplo)
                if (fila + col) % 2 != 0:
                    if fila < 3:
                        self.matriz[fila][col].ficha = Ficha(Usuario.J1, Tipo.FICHA, Estado.JUGABLE)
                    elif fila > 4:
                        self.matriz[fila][col].ficha = Ficha(Usuario.J2, Tipo.FICHA, Estado.JUGABLE)

    def validar_movimiento(self, turno: bool, origen: Casilla, destino: Casilla) -> bool:
        # Aquí implementas tu lógica de movimiento según tipo de ficha y jugador
        # Retorna True si es válido, False si no
        return True

    def verificar_victoria(self) -> bool | None:
        # Retorna "roja", "azul" o None si nadie ha ganado
        return None


# Ejemplo de uso
tablero = TableroLogico()

