from .Estado import *
from .Tipo import *
from .Usuario import *
from .Ficha import *
from .Casilla import *



# Clase tablero
class TableroLogico:

    def __init__(self):
        self.puede_concatenar = False
        self.matriz = [[Casilla(fila, col, None) for col in range(8)] for fila in range(8)]
        self.turno = Usuario.J1
        self.generar_casillas_con_fichas()

    def generar_casillas_con_fichas(self):
        for fila in range(8):
            for col in range(8):
                # Solo en casillas negras (por ejemplo)
                if (fila + col) % 2 != 0:
                    if fila < 3:
                        self.matriz[fila][col].ficha = Ficha(Usuario.J2, Tipo.FICHA, Estado.JUGABLE)
                    elif fila > 4:
                        self.matriz[fila][col].ficha = Ficha(Usuario.J1, Tipo.FICHA, Estado.JUGABLE)

    def validar_movimiento(self, origen: Casilla, destino: Casilla) -> bool:
        if origen.ficha is not None and destino.ficha is None:
            # Definir dirección y enemigo según el jugador
            if self.turno == Usuario.J1:
                direccion = -1  # J1 avanza hacia arriba
                enemigo = Usuario.J2
            else:
                direccion = 1  # J2 avanza hacia abajo
                enemigo = Usuario.J1

            fila_diff = destino.fila - origen.fila
            columna_diff = destino.columna - origen.columna
            abs_diff_fila = abs(fila_diff)
            abs_diff_columna = abs(columna_diff)

            # Para fichas normales, solo avanzan hacia adelante
            if origen.ficha.tipo == Tipo.FICHA and fila_diff * direccion < 0:
                return False  # No puede moverse hacia atrás

            # Movimiento simple de 1
            if abs_diff_fila == 1 and abs_diff_columna == 1:
                if abs_diff_fila == 1 and abs_diff_columna == 1:
                    destino.ficha = origen.ficha  # Mover ficha
                    origen.ficha = None  # Limpiar origen
                    self.turno = Usuario.J2 if self.turno == Usuario.J1 else Usuario.J1
                    return True

            # Movimiento de salto de 2
            elif abs_diff_fila == 2 and abs_diff_columna == 2:
                mid_fila = origen.fila + fila_diff // 2
                mid_col = origen.columna + columna_diff // 2
                if (self.matriz[mid_fila][mid_col].ficha is not None and
                        self.matriz[mid_fila][mid_col].ficha.usuario == enemigo):
                    self.matriz[mid_fila][mid_col].ficha = None
                    destino.ficha = origen.ficha  # Mover ficha
                    origen.ficha = None  # Limpiar origen
                    self.concatenar(destino, enemigo)
                    return True
        return False

    def concatenar(self, nuevo_origen: Casilla, enemigo: Usuario) -> bool:
        filas = len(self.matriz)
        cols = len(self.matriz[0])

        # Movimiento abajo a la derecha
        if nuevo_origen.fila + 2 < filas and nuevo_origen.columna + 2 < cols:
            if self.matriz[nuevo_origen.fila + 2][nuevo_origen.columna + 2].ficha is None:
                mid_fila = nuevo_origen.fila + (
                            self.matriz[nuevo_origen.fila + 2][nuevo_origen.columna + 2].fila - nuevo_origen.fila) // 2
                mid_col = nuevo_origen.columna + (self.matriz[nuevo_origen.fila + 2][
                                                      nuevo_origen.columna + 2].columna - nuevo_origen.columna) // 2
                if self.matriz[mid_fila][mid_col].ficha is not None and self.matriz[mid_fila][
                    mid_col].ficha.usuario == enemigo:
                    self.puede_concatenar = True

        # Movimiento abajo a la izquierda
        if nuevo_origen.fila + 2 < filas and nuevo_origen.columna - 2 >= 0:
            if self.matriz[nuevo_origen.fila + 2][nuevo_origen.columna - 2].ficha is None:
                mid_fila = nuevo_origen.fila + (
                            self.matriz[nuevo_origen.fila + 2][nuevo_origen.columna - 2].fila - nuevo_origen.fila) // 2
                mid_col = nuevo_origen.columna + (self.matriz[nuevo_origen.fila + 2][
                                                      nuevo_origen.columna - 2].columna - nuevo_origen.columna) // 2
                if self.matriz[mid_fila][mid_col].ficha is not None and self.matriz[mid_fila][
                    mid_col].ficha.usuario == enemigo:
                    self.puede_concatenar = True

        # Movimiento arriba a la derecha
        if nuevo_origen.fila - 2 >= 0 and nuevo_origen.columna + 2 < cols:
            if self.matriz[nuevo_origen.fila - 2][nuevo_origen.columna + 2].ficha is None:
                mid_fila = nuevo_origen.fila + (
                            self.matriz[nuevo_origen.fila - 2][nuevo_origen.columna + 2].fila - nuevo_origen.fila) // 2
                mid_col = nuevo_origen.columna + (self.matriz[nuevo_origen.fila - 2][
                                                      nuevo_origen.columna + 2].columna - nuevo_origen.columna) // 2
                if self.matriz[mid_fila][mid_col].ficha is not None and self.matriz[mid_fila][
                    mid_col].ficha.usuario == enemigo:
                    self.puede_concatenar = True

        # Movimiento arriba a la izquierda
        if nuevo_origen.fila - 2 >= 0 and nuevo_origen.columna - 2 >= 0:
            if self.matriz[nuevo_origen.fila - 2][nuevo_origen.columna - 2].ficha is None:
                mid_fila = nuevo_origen.fila + (
                            self.matriz[nuevo_origen.fila - 2][nuevo_origen.columna - 2].fila - nuevo_origen.fila) // 2
                mid_col = nuevo_origen.columna + (self.matriz[nuevo_origen.fila - 2][
                                                      nuevo_origen.columna - 2].columna - nuevo_origen.columna) // 2
                if self.matriz[mid_fila][mid_col].ficha is not None and self.matriz[mid_fila][
                    mid_col].ficha.usuario == enemigo:
                    self.puede_concatenar = True

        # Si no puede concatenar el turno cambia
        if not self.puede_concatenar:
            self.turno = enemigo
            return False

        return True

    def puede_mover(self, jugador, rival: Usuario) -> bool:
        filas = len(self.matriz)
        cols = len(self.matriz[0])

        for fila in range(filas):
            for col in range(cols):
                if self.matriz[fila][col].ficha is not None and self.matriz[fila][col].ficha.usuario == jugador:
                    origen = self.matriz[fila][col]

                    if fila + 1 < filas and col + 1 < cols:
                        if self.matriz[fila + 1][col + 1].ficha is None:
                            return True
                    if fila + 1 < filas and col - 1 >= 0:
                        if self.matriz[fila + 1][col - 1].ficha is None:
                            return True
                    if fila - 1 >= 0 and col + 1 < cols:
                        if self.matriz[fila - 1][col + 1].ficha is None:
                            return True
                    if fila - 1 >= 0 and col - 1 >= 0:
                        if self.matriz[fila - 1][col - 1].ficha is None:
                            return True
        return False

    def puede_comer(self, jugador: Usuario, rival: Usuario) -> bool:
        filas = len(self.matriz)
        cols = len(self.matriz[0])

        for fila in range(filas):
            for col in range(cols):
                if self.matriz[fila][col].ficha.usuario == jugador:
                    origen = self.matriz[fila][col]

                    # Movimiento abajo a la derecha
                    if fila + 2 < filas and col + 2 < cols:
                        if self.matriz[fila + 2][col + 2].ficha is None:
                            mid_fila = fila + 1
                            mid_col = col + 1
                            if self.matriz[mid_fila][mid_col].ficha == rival:
                                return True

                    # Movimiento abajo a la izquierda
                    if fila + 2 < filas and col - 2 >= 0:
                        if self.matriz[fila + 2][col - 2].ficha is None:
                            mid_fila = fila + 1
                            mid_col = col - 1
                            if self.matriz[mid_fila][mid_col].ficha == rival:
                                return True

                    # Movimiento arriba a la derecha
                    if fila - 2 >= 0 and col + 2 < cols:
                        if self.matriz[fila - 2][col + 2].ficha is None:
                            mid_fila = fila - 1
                            mid_col = col + 1
                            if self.matriz[mid_fila][mid_col].ficha == rival:
                                return True

                    # Movimiento arriba a la izquierda
                    if fila - 2 >= 0 and col - 2 >= 0:
                        if self.matriz[fila - 2][col - 2].ficha is None:
                            mid_fila = fila - 1
                            mid_col = col - 1
                            if self.matriz[mid_fila][mid_col].ficha == rival:
                                return True
        return False


# Ejemplo de uso
tablero = TableroLogico()

