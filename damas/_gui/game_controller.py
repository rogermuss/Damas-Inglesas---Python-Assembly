from PyQt6 import QtCore, QtGui, QtWidgets
from damas._gui.Tablero import Ui_MainWindow

class Game(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Inicializar tamaño de la ventana
        self.resize(750, 700)

        # Llama a la funcion crear_tablero()
        self.crear_tablero()

    def crear_tablero(self):
        for fila in range(8):
            for col in range(8):
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
                if color == "#2E2E2E" and (fila < 3 or fila > 4):
                    label_ficha = QtWidgets.QLabel()
                    label_ficha.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    if fila < 3:
                        label_ficha.setProperty("jugable", True)
                        pixmap = QtGui.QPixmap("_resources/PiezaAzul.png")
                    else:
                        label_ficha.setProperty("jugable", False)
                        pixmap = QtGui.QPixmap("_resources/PiezaRoja.png")
                    label_ficha.setPixmap(pixmap.scaled(50, 50,
                                                        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                        QtCore.Qt.TransformationMode.SmoothTransformation))
                    layout.addWidget(label_ficha)

                # Activar eventos si es casilla jugable
                if color == "#2E2E2E":
                    self.activar_eventos_casilla(casilla, fila, col)

                self.grid.addWidget(casilla, fila, col)

        for i in range(8):
            self.grid.setColumnStretch(i, 1)
            self.grid.setRowStretch(i, 1)

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
