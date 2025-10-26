from Ficha import *

class Casilla:
    def __init__(self, fila: int, columna: int, ficha: Ficha | None):
        self.ficha = ficha
        self.fila = fila
        self.columna = columna


    def setFicha(self, ficha: Ficha):
        self.ficha = ficha

    def setFila(self, ficha: Ficha):
        self.ficha = ficha

    def setColumna(self, columna: int):
        self.columna = columna

    def getFicha(self):
        return self.ficha

    def getFila(self):
        return self.ficha

    def getColumna(self):
        return self.ficha
