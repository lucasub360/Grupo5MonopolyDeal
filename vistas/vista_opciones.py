from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QFrame, QMessageBox
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class Opciones(QDialog):
    def __init__(self, controlador, parent=None):
        super().__init__(parent)

        self.__controlador = controlador
        
        self.setWindowTitle("Opciones")
        self.setGeometry(570, 240, 400, 300)
        self.setWindowIcon(QIcon("imagenes/ui/icono.png"))

        #Layout
        self.layout = QVBoxLayout()
        self.layout_para_centrar_botones = QVBoxLayout()
        self.layout.addSpacing(10)

        #Titulo
        self.label = QLabel("Ajustes y configuraciones del juego:", self)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(20)

        #Linea
        linea1 = QFrame(self)
        linea1.setFrameShape(QFrame.Shape.HLine)
        linea1.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(linea1)

        self.layout.addSpacing(10)

        #Botones a,b,c ------------
        boton_a = QPushButton("Version prémium", self)
        boton_a.setFixedWidth(250)
        boton_a.setEnabled(False)

        boton_b = QPushButton("Recompensa diaria", self)
        boton_b.setFixedWidth(250)
        boton_b.setEnabled(False)

        boton_c = QPushButton("Activar cheats", self)
        boton_c.setFixedWidth(250)
        boton_c.setEnabled(False)
        #------------

        self.layout_para_centrar_botones.addWidget(boton_a, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_para_centrar_botones.addSpacing(2)
        self.layout_para_centrar_botones.addWidget(boton_b, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_para_centrar_botones.addSpacing(2)
        self.layout_para_centrar_botones.addWidget(boton_c, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.layout_para_centrar_botones)
        self.layout.addSpacing(10)
        
        #Otra Linea: 
        linea1 = QFrame(self)
        linea1.setFrameShape(QFrame.Shape.HLine)
        linea1.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(linea1)

        self.layout.addSpacing(10)

        # Boton Créditos:
        boton_creditos = QPushButton("Créditos", self)
        boton_creditos.clicked.connect(self.mostrar_creditos)
        self.layout.addWidget(boton_creditos)

        self.layout.addSpacing(10)

        #Otra Linea: 
        linea1 = QFrame(self)
        linea1.setFrameShape(QFrame.Shape.HLine)
        linea1.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(linea1)

        self.layout.addSpacing(10)

        # Volver:
        self.boton_volver = QPushButton("Volver al Menú Principal", self)
        self.boton_volver.clicked.connect(self.__controlador.volver)
        self.layout.addWidget(self.boton_volver)
        self.setLayout(self.layout) 

    def mostrar_creditos(self):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Créditos")
        mensaje.setText("Nosotros desarrollamos este juego:")
        mensaje.setInformativeText(
            "\n\nBonifacio, Lucas\n"
            "Cárdenas, Franco\n"
            "Lopes, Carlos\n"
            "Gonzales, Nadin\n"
            "Cabana, Ricardo (Abandonó)\n"
            "Williams, Dahiana\n"
            "Vidal, Maida Diego\n"
            "Ampuero, Alejandro\n"
            "Contreras, Joel\n")
        mensaje.setIcon(QMessageBox.Icon.Information)
        mensaje.setStandardButtons(QMessageBox.StandardButton.Ignore)
        mensaje.exec()

    def centrar_ventana(self):
        forma_pantalla = QGuiApplication.primaryScreen().availableGeometry()
        forma_ventana = self.frameGeometry()
        centro_pantalla = forma_pantalla.center()
        forma_ventana.moveCenter(centro_pantalla)
        self.move(forma_ventana.topLeft())
