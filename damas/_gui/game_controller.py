from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLabel
from _logica.TableroLogico import *
from _logica.Usuario import *

from damas._gui.Tablero import Ui_MainWindow

class Game(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Inicializar tamaño de la ventana
        self.setFixedSize(800, 724)
        # Llama a la funcion crear_tablero()
        self.crear_tablero()
        self.tableroLogico = TableroLogico()

    def crear_tablero(self):
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
                    if color == "#2E2E2E" and col > 0 and (0 < fila < 4 or fila > 5):
                        label_ficha = QtWidgets.QLabel()
                        label_ficha.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        if 0 < fila < 4:
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

    def click_casilla(self, event, fila, col):
        print(f"Click en casilla ({fila}, {col})")

    def unhover_casilla(self, event, fila, col):
        print(f"Unhover en casilla ({fila}, {col})")

    def hover_casilla(self, event, fila, col):
        print(f"Hover en casilla ({fila}, {col})")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Game()
    ventana.show()
    sys.exit(app.exec())
