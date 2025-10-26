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

        self.actionNew_Game.triggered.connect(self.reiniciar_juego)
        # Llama a la funcion crear_tablero()
        self.tableroLogico = TableroLogico()
        self.crear_tablero()

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


    def actualizar_fichas(self):
        for fila in range(1, 9):
            for col in range(1, 9):
                casilla_widget = self.gridLayout_2.itemAtPosition(fila, col).widget()
                if casilla_widget and (fila + col) % 2 != 0:  # Solo casillas negras
                    # Limpiar layout de la casilla
                    layout = casilla_widget.layout()
                    while layout.count():
                        item = layout.takeAt(0)
                        if item.widget():
                            item.widget().deleteLater()

                    # Agregar ficha si existe
                    ficha = self.tableroLogico.matriz[fila - 1][col - 1].ficha
                    if ficha is not None:
                        label_ficha = QtWidgets.QLabel()
                        label_ficha.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        label_ficha.setStyleSheet("background: transparent; border: none;")
                        label_ficha.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

                        if ficha.usuario == Usuario.J2:
                            if ficha.tipo == Tipo.FICHA:
                                pixmap = QtGui.QPixmap("_resources/PiezaAzul.png")
                            else:
                                pixmap = QtGui.QPixmap("_resources/PiezaMorada.png")
                        else:
                            if ficha.tipo == Tipo.FICHA:
                                pixmap = QtGui.QPixmap("_resources/PiezaRoja.png")
                            else:
                                pixmap = QtGui.QPixmap("_resources/PiezaAmarilla.png")

                        label_ficha.setPixmap(pixmap.scaled(50, 50,
                                                            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                            QtCore.Qt.TransformationMode.SmoothTransformation))
                        layout.addWidget(label_ficha)


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

    def returnDefault(self):
        if self.contenedor_seleccionado is not None:
            fila_seleccionada = self.contenedor_seleccionado.fila + 1
            col_seleccionada = self.contenedor_seleccionado.columna + 1
            casilla = self.gridLayout_2.itemAtPosition(fila_seleccionada, col_seleccionada).widget()

            if casilla:
                original_color = "#2E2E2E" if (fila_seleccionada + col_seleccionada) % 2 != 0 else "#E6E6E6"
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
                    background-color: #A3C1E0;  /* azul pastel */
                    border-width: 3px;
                    border-style: solid;
                    border-color: #4C7BB8;  /* azul más intenso */
                    border-radius: 4px;
                """)

            self.contenedor_seleccionado = casilla_logica
            print(f"Click permitido en casilla ({fila}, {col})")
        else:
            if self.contenedor_seleccionado is not None:
                if self.contenedor_seleccionado is self.tableroLogico.matriz[fila - 1][col - 1]:
                    self.contenedor_seleccionado = None
                    casilla = self.gridLayout_2.itemAtPosition(fila, col).widget()
                    original_color = "#2E2E2E" if (fila + col) % 2 != 0 else "#E6E6E6"
                    casilla.setStyleSheet(f"background-color: {original_color};")
                    return

                if self.tableroLogico.validar_movimiento(self.contenedor_seleccionado, casilla_logica):
                    if not self.tableroLogico.puede_mover_o_comer():
                      self.mostrar_mensaje_derrota(self.tableroLogico.turno)
                    self.actualizar_fichas()
                    self.returnDefault()
                    self.contenedor_seleccionado = None

    def mostrar_mensaje_derrota(self, perdedor: Usuario):
        """Muestra un mensaje de derrota/victoria y pregunta si quiere jugar de nuevo"""
        from PyQt6.QtWidgets import QMessageBox

        # Determinar el mensaje según el ganador
        if perdedor == Usuario.J2:
            titulo = "¡Jugador 1 (Rojo) ha ganado!"
            mensaje = "El Jugador 2 (Azul) no tiene más movimientos válidos."
        else:
            titulo = "¡Jugador 2 (Azul) ha ganado!"
            mensaje = "El Jugador 1 (Rojo) no tiene más movimientos válidos."

        # Crear el mensaje
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setInformativeText("¿Deseas jugar de nuevo?")
        msg_box.setIcon(QMessageBox.Icon.Information)

        # Agregar botones personalizados
        btn_si = msg_box.addButton("Jugar de nuevo", QMessageBox.ButtonRole.AcceptRole)
        btn_no = msg_box.addButton("Salir", QMessageBox.ButtonRole.RejectRole)

        # Mostrar el diálogo y esperar respuesta
        msg_box.exec()

        # Verificar qué botón se presionó
        if msg_box.clickedButton() == btn_si:
            self.reiniciar_juego()
        else:
            self.close()  # Cierra la ventana

    def reiniciar_juego(self):
        """Reinicia el juego a su estado inicial"""
        # Resetear lógica del tablero
        self.tableroLogico = TableroLogico()
        self.contenedor_seleccionado = None

        # Limpiar el gridLayout
        while self.gridLayout_2.count():
            item = self.gridLayout_2.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Recrear el tablero
        self.crear_tablero()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Game()
    ventana.show()
    sys.exit(app.exec())
