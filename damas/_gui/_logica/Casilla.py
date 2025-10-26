from .Ficha import *

class Casilla:
    def __init__(self, fila: int, columna: int, ficha: Ficha | None):
        self.ficha = ficha
        self.fila = fila
        self.columna = columna

    def getFila(self):
        return self.fila  # Cambio aquí

    def getColumna(self):
        return self.columna

    def setColumna(self, columna: int):
        self.columna = columna

    def getFicha(self):
        return self.ficha

    def getFila(self):
        return self.ficha

    def getColumna(self):
        return self.ficha
