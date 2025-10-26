from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLabel
from _logica.TableroLogico import *
from _logica.Usuario import *

from damas._gui.Tablero import Ui_MainWindow

class Game(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.contenedor_seleccionado = None

        super().__init__()
        self.setupUi(self)
        # Inicializar tamaño de la ventana
        self.setFixedSize(800, 724)
        # Llama a la funcion actualizar_tablero()
        self.tableroLogico = TableroLogico()
        self.actualizar_tablero()

    def actualizar_tablero(self):
        for fila in range(9):
            for col in range(9):
                if fila == 0 and col == 0:
                    pass
                elif (fila == 0) ^ (col == 0):
                    if fila == 0:
                        label = QLabel(str(col))
                    else:
                        label = QLabel(str(fila))
                    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    label.setStyleSheet("font-weight: bold; font-size: 14px;")
                    self.gridLayout_2.addWidget(label, fila, col)
                else:
                    casilla = QtWidgets.QFrame()
                    color = "#E6E6E6" if (fila + col) % 2 == 0 else "#2E2E2E"
                    casilla.setStyleSheet(f"background-color: {color};")
                    casilla.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                      QtWidgets.QSizePolicy.Policy.Expanding)

                    layout = QtWidgets.QVBoxLayout(casilla)
                    layout.setContentsMargins(0, 0, 0, 0)
                    layout.setSpacing(0)
                    layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)





                # Colocar imagen en casillas negras
                    ficha = self.tableroLogico.matriz[fila-1][col-1].ficha

                    if ficha is not None:
                        label_ficha = QtWidgets.QLabel()
                        label_ficha.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        label_ficha.setStyleSheet("background: transparent; border: none;")
                        label_ficha.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
                        if ficha.usuario == Usuario.J2:
                            label_ficha.setProperty("jugable", Usuario.J2)
                            pixmap = QtGui.QPixmap("_resources/PiezaAzul.png")
                        else:
                            label_ficha.setProperty("jugable", Usuario.J1)
                            pixmap = QtGui.QPixmap("_resources/PiezaRoja.png")
                        label_ficha.setPixmap(pixmap.scaled(50, 50,
                                                        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                        QtCore.Qt.TransformationMode.SmoothTransformation))
                        layout.addWidget(label_ficha)

                    # Activar eventos si es casilla jugable
                    if color == "#2E2E2E" and fila > 0 and col > 0:
                        self.activar_eventos_casilla(casilla, fila, col)

                    self.gridLayout_2.addWidget(casilla, fila, col)

            for i in range(9):
                self.gridLayout_2.setColumnStretch(i, 1)
                self.gridLayout_2.setRowStretch(i, 1)


    # Función para activar hover y click en una casilla
    def activar_eventos_casilla(self, casilla, fila, col):
        casilla.setProperty("jugable", True)
        casilla.setMouseTracking(True)  # necesario para hover
        casilla.enterEvent = lambda event: self.hover_casilla(event, fila, col)
        casilla.leaveEvent = lambda event: self.unhover_casilla(event, fila, col)
        casilla.mousePressEvent = lambda event: self.click_casilla(event, fila, col)




    def hover_casilla(self, event, fila, col):
        casilla = self.gridLayout_2.itemAtPosition(fila, col).widget()
        ficha = self.tableroLogico.matriz[fila - 1][col - 1].ficha  # lógica no considera numeración
        if ficha is not None and ficha.usuario == self.tableroLogico.turno:
            if self.contenedor_seleccionado is not self.tableroLogico.matriz[fila - 1][col - 1]:
                if self.tableroLogico.turno == Usuario.J1:
                    casilla.setStyleSheet("background-color: #B84C4C;")
                else:
                    casilla.setStyleSheet("background-color: #4C7BB8;")
        else:
            original_color = "#2E2E2E"
            casilla.setStyleSheet(f"background-color: {original_color};")



    def unhover_casilla(self, event, fila, col):
        if self.contenedor_seleccionado is not self.tableroLogico.matriz[fila - 1][col - 1]:
            casilla = self.gridLayout_2.itemAtPosition(fila, col).widget()
            original_color = "#2E2E2E" if (fila + col) % 2 != 0 else "#E6E6E6"
            casilla.setStyleSheet(f"background-color: {original_color};")





    def click_casilla(self, event, fila, col):
        casilla_logica = self.tableroLogico.matriz[fila - 1][col - 1]

        # widget en esa posicion del layout
        casilla = self.gridLayout_2.itemAtPosition(fila, col).widget()

        if (casilla_logica.ficha is not None and casilla_logica.ficha.usuario == self.tableroLogico.turno
            and self.contenedor_seleccionado is None):

            if self.tableroLogico.turno == Usuario.J1:
                casilla.setStyleSheet("""
                    background-color: #FF6F61;
                    border-width: 3px;
                    border-style: solid;
                    border-color: #B84C4C;
                    border-radius: 4px;
                """)
            else:
                casilla.setStyleSheet("""
                    background-color: #4C7BB8;
                    border-width: 3px;
                    border-style: solid;
                    border-image: linear-gradient(to right, #1E3A6B, #4C7BB8) 1;
                    border-radius: 4px;
                """)
            self.contenedor_seleccionado = casilla_logica
            print(f"Click permitido en casilla ({fila}, {col})")
        else:
            if self.contenedor_seleccionado is self.tableroLogico.matriz[fila - 1][col - 1]:
                self.contenedor_seleccionado = None
                casilla = self.gridLayout_2.itemAtPosition(fila, col).widget()
                original_color = "#2E2E2E" if (fila + col) % 2 != 0 else "#E6E6E6"
                casilla.setStyleSheet(f"background-color: {original_color};")
                return

            if tablero.validar_movimiento(self.contenedor_seleccionado, casilla_logica):
                self.actualizar_tablero()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Game()
    ventana.show()
    sys.exit(app.exec())
