from Usuario import *
from Tipo import *
from Estado import *

class Ficha:

    def __init__(self, usuario: Usuario, tipo: Tipo, estado: Estado):
        self.usuario = usuario
        self.tipo = tipo
        self.estado = estado

    def getUsuario(self):
        return self.usuario
    def getTipo(self):
        return self.tipo
    def getEstado(self):
        return self.estado

    def setUsuario(self, usuario: Usuario):
        self.usuario = usuario
    def setTipo(self, tipo: Tipo):
        self.tipo = tipo
    def setEstado(self, estado: Estado):
        self.estado = estado

