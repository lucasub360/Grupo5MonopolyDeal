from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QApplication
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from crear_partida import CrearPartida
from opciones import Opciones
from como_juego import ComoJuego

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monopoly Deal")
        self.setGeometry(480, 200, 600, 450)
        self.setWindowIcon(QIcon("imagenes/ui/icono.png"))

        # Configuración del sonido: <-- Tutorial en Stack Overflow
        self.filename = "imagenes/sonido/click.wav"
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(self.filename))
        self.audio_output.setVolume(50)

        # Widget principal y layout:
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # (1):
        # Espaciador superior:
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # (2):
        # Imagen encabezado:
        self.imagen_label = QLabel(self)
        pixmap = QPixmap("imagenes/ui/headerLogo.png").scaled(
            400, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        self.imagen_label.setPixmap(pixmap)
        self.imagen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.imagen_label)

        # (3):
        # Espaciador inferior:
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # (4):
        # Botones:
        botones_layout = QVBoxLayout()
        botones_layout.setContentsMargins(30, 0, 30, 20) # <-- Márgenes!!!

        # (4.1):
        # Botón "Crear una Partida":
        self.boton_crear_partida = self.crear_boton("Crear una Partida", "imagenes/ui/menu_boton_1.png")
        self.boton_crear_partida.clicked.connect(self.mostrar_crear_partida)
        botones_layout.addWidget(self.boton_crear_partida)

        botones_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # (4.2):
        # Botón "Opciones":
        self.boton_opciones = self.crear_boton("Opciones", "imagenes/ui/menu_boton_2.png")
        self.boton_opciones.clicked.connect(self.mostrar_opciones)
        botones_layout.addWidget(self.boton_opciones)

        botones_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # (4.3):
        # Botón "Iniciar Sesión o Crear Usuario":
        self.boton_iniciar_sesion = self.crear_boton("¿Cómo Juego?", "imagenes/ui/smiley.png")
        self.boton_iniciar_sesion.clicked.connect(self.mostrar_como_juego)
        botones_layout.addWidget(self.boton_iniciar_sesion)

        # Agregar los 3 botones al layout principal:
        self.layout.addLayout(botones_layout)

        # ---

        # Las instancias de las ventanas secundarias:
        self.crear_partida_window = CrearPartida(self)
        self.opciones_window = Opciones(self)
        self.como_juego_window = ComoJuego(self)

    def crear_boton(self, texto, icono_ruta):
        """Crea un botón que tiene un ícono (a la izquierda) y texto."""
        boton = QPushButton(self) # <-- Este es el contenedor principal.
        boton.setStyleSheet("""
            QPushButton {
                border: 2px solid #444;
                border-radius: 10px;
                background-color: #222; /* <-- Es perfecto no cambiar */
                font-size: 20px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #333; /* <-- Tampoco */
            }
        """)
        boton.setMinimumWidth(400)
        boton.setFixedHeight(60)

        # Layout del ícono y el texto:
        layout = QHBoxLayout(boton)

        # Ícono
        icono_label = QLabel(self)
        pixmap = QPixmap(icono_ruta).scaled(30, 30) # <-- Tamaño de la imagen.
        icono_label.setPixmap(pixmap)
        icono_label.setFixedSize(100, 40)           # <-- Tamaño fijo del contenedor del ícono.
        layout.addWidget(icono_label)

        # Texto
        texto_label = QLabel(texto, self)
        texto_label.setStyleSheet("""
            font-size: 20px;        /* <-- Hace una re diferencia */
        """)
        layout.addWidget(texto_label)

        return boton

    def sonido_click(self):
        self.player.stop()
        self.player.play()

    def mostrar_crear_partida(self):
        self.sonido_click()
        self.hide()
        self.crear_partida_window.exec()

    def mostrar_opciones(self):
        self.sonido_click()
        self.hide()
        self.opciones_window.exec()

    def mostrar_como_juego(self):
        self.sonido_click()
        self.hide()
        self.como_juego_window.exec()