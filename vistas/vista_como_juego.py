












# No le den bola todavía, lo estoy haciendo (boni)











from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QFrame, QMessageBox, QScrollArea
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

class ComoJuego(QDialog):
    def __init__(self, main_menu, parent=None):
        super().__init__(parent)
        self.main_menu = main_menu
        self.setWindowTitle("¿Cómo Juego?")
        self.setGeometry(340, 130, 900, 600)
        self.setWindowIcon(QIcon("imagenes/ui/icono.png"))
        self.centrar_ventana()

        # ---
        
        # Main layout:
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # Widgets:
        self.widget_arriba = QWidget()
        self.widget_abajo = QWidget()
        
        # Scroller:
        self.scroll_area_abajo = QScrollArea(self)
        self.scroll_area_abajo.setWidgetResizable(True)
        
        # Estilos de los widgets:
        #self.widget_arriba.setStyleSheet("""
        #    background-color: rgba(89, 45, 22, 1);
        #    border-bottom: 3px solid rgba(72, 26, 11, 1);
        #""")
        self.scroll_area_abajo.setObjectName("scrollerAbajo") # <-- Así lo de adentro no hereda el diseño.
        self.scroll_area_abajo.setStyleSheet("""
            #scrollerAbajo {
                border: 2px solid #444;
                border-radius: 5px;
                background-color: #222;
                font-size: 18px;
                text-align: left;
                padding: 5px;
            }
        """)
        #self.widget_abajo.setFixedHeight(500)
        
        # Layouts (Les paso los Widgets):
        self.layout_arriba = QVBoxLayout(self.widget_arriba)
        self.layout_arriba.setContentsMargins(0, 0, 0, 0)
        self.layout_arriba.setSpacing(0)
        
        self.layout_arriba_arriba = QHBoxLayout()
        self.layout_arriba_arriba.setContentsMargins(10, 10, 0, 0)
        self.layout_arriba_arriba.setSpacing(0)
        self.layout_arriba_arriba.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.layout_arriba_abajo = QHBoxLayout()
        self.layout_arriba_abajo.setContentsMargins(20, 10, 20, 10)
        self.layout_arriba_abajo.setSpacing(12)
        self.layout_arriba_abajo.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        self.layout_abajo = QVBoxLayout(self.widget_abajo)
        self.layout_abajo.setContentsMargins(10, 10, 10, 10)
        self.layout_abajo.setSpacing(5)
        self.layout_abajo.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # El layout_abajo cambia dinámicamente.
        self.mostrar_reglas_generales() # <-- Acá me aseguro que empiece con la de Reglas Generales como predeterminado.
        
        # ---
        
        # Volver:
        self.boton_volver = self.crear_boton_volver("Volver", "imagenes/ui/home.png")
        self.boton_volver.clicked.connect(self.volver)
        self.layout_arriba_arriba.addWidget(self.boton_volver)
        
        # ---
        
        # Botón "Reglas Generales":
        self.boton_reglas_generales = self.crear_boton("Reglas Generales", "imagenes/ui/book_question.png")
        self.boton_reglas_generales.clicked.connect(self.mostrar_reglas_generales)
        self.layout_arriba_abajo.addWidget(self.boton_reglas_generales)
        
        # Botón "Ver las Cartas":
        self.boton_ver_cartas = self.crear_boton("Ver las Cartas", "imagenes/ui/blogs_stack.png")
        self.boton_ver_cartas.clicked.connect(self.mostrar_ver_cartas)
        self.layout_arriba_abajo.addWidget(self.boton_ver_cartas)
        
        # Botón "A cerca de la Interfaz":
        self.boton_a_cerca_interfaz = self.crear_boton("A cerca de la Interfaz", "imagenes/ui/checkerboard.png")
        self.boton_a_cerca_interfaz.clicked.connect(self.mostrar_a_cerca_interfaz)
        self.layout_arriba_abajo.addWidget(self.boton_a_cerca_interfaz)

        # ---
        
        # Lo de arriba:
        self.layout_arriba.addLayout(self.layout_arriba_arriba)
        self.layout_arriba.addLayout(self.layout_arriba_abajo)
        self.main_layout.addWidget(self.widget_arriba)
        
        # Lo de abajo:
        self.scroll_area_abajo.setWidget(self.widget_abajo)
        self.main_layout.addWidget(self.scroll_area_abajo) # <-- Lo dinámico es lo que va adentro, sirve para darle estilo.
    
    def crear_boton(self, texto, icono_ruta):
        """Crea un botón que tiene un ícono (a la izquierda) y texto."""
        boton = QPushButton(self) # <-- Este es el contenedor principal.
        boton.setStyleSheet("""
            QPushButton {
                border: 2px solid #444;
                border-radius: 5px;
                background-color: #222; /* <-- Es perfecto no cambiar */
                font-size: 18px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #333; /* <-- Tampoco */
            }
        """)
        boton.setFixedHeight(50)
        boton.setFixedWidth(250)

        # Layout del ícono y el texto:
        layout = QHBoxLayout(boton)

        # Ícono
        icono_label = QLabel(self)
        pixmap = QPixmap(icono_ruta).scaled(20, 20) # <-- Tamaño de la imagen.
        icono_label.setPixmap(pixmap)
        icono_label.setFixedSize(20, 20)            # <-- Tamaño fijo del contenedor del ícono.
        layout.addWidget(icono_label)

        # Texto
        texto_label = QLabel(texto, self)
        texto_label.setStyleSheet("""
            padding-left: 5px;
            font-size: 18px;
        """)
        layout.addWidget(texto_label)

        return boton
    
    def crear_boton_volver(self, texto, icono_ruta):
        """Crea un botón que tiene un ícono (a la izquierda) y texto."""
        boton = QPushButton(self) # <-- Este es el contenedor principal.
        boton.setStyleSheet("""
            QPushButton {
                border: 2px solid #444;
                border-radius: 3px;
                background-color: #222; /* <-- Es perfecto no cambiar */
                font-size: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #333; /* <-- Tampoco */
            }
        """)
        boton.setFixedHeight(30)
        boton.setFixedWidth(175)

        # Layout del ícono y el texto:
        layout = QHBoxLayout(boton)

        # Ícono
        icono_label = QLabel(self)
        pixmap = QPixmap(icono_ruta).scaled(15, 15) # <-- Tamaño de la imagen.
        icono_label.setPixmap(pixmap)
        icono_label.setFixedSize(15, 15)            # <-- Tamaño fijo del contenedor del ícono.
        layout.addWidget(icono_label)

        # Texto
        texto_label = QLabel(texto, self)
        texto_label.setStyleSheet("""
            padding-left: 5px;
            font-size: 16px;
        """)
        layout.addWidget(texto_label)

        return boton
    
    def limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater() # <-- Borrar el Widget.
            elif item.layout():
                self.limpiar_layout(item.layout()) # <-- (En caso de que hayan Widgets anidados).
    
    def mostrar_reglas_generales(self):
        self.limpiar_layout(self.layout_abajo)
        
        linea1 = QLabel("¡Bienvenido a Monopoly Deal de Escritorio!")
        linea1.setStyleSheet("""
            padding-left: 5px;
            font-size: 22px;
        """)
        
        linea2 = QLabel("En este tutorial aprenderás como jugar y ganar.")
        
        separador1 = QFrame(self)
        separador1.setFrameShape(QFrame.Shape.HLine)
        separador1.setFrameShadow(QFrame.Shadow.Sunken)
        
        linea3 = QLabel("1. Mazo:")
        linea3.setStyleSheet("""
            color: #74F1FF;
            font-size: 18px;
        """)
        
        linea4 = QLabel("Cada jugador comienza la partida con <u>5 cartas aleatorias</u> en su mazo, el mazo puede tener un máximo de 7 cartas.")
        linea5 = QLabel("Cuando sea tu turno <u>agarrá cartas</u> y agregalas a tu mazo:")
        linea6 = QLabel("  -  Caso 1: Agarrá 2 cartas.")
        linea7 = QLabel("  -  Caso 2: No tenés cartas en tu mazo, entonces agarrá 5 en vez de 2.")
        linea8 = QLabel("Cuando sea tu turno <u>podés jugar cartas</u>, te recomendamos este órden:")
        linea9 = QLabel("  -  A. Cartas de Dinero.")
        linea10 = QLabel("  -  B. Cartas de Propiedad.")
        linea11 = QLabel("  -  C. Cartas de Acción (<-- Solo podés jugar 1 carta de acción por turno).")
        
        separador2 = QFrame(self)
        separador2.setFrameShape(QFrame.Shape.HLine)
        separador2.setFrameShadow(QFrame.Shadow.Sunken)
        
        linea12 = QLabel("2. Finalizá tu Turno:")
        linea12.setStyleSheet("""
            color: #E1A3FF;
            font-size: 18px;
        """)
        
        linea13 = QLabel("Una vez termines tus movimientos pasá el turno para que otro juegue.")
        linea14 = QLabel("Si el tiempo supera los 60s se cambiará solo el turno, así que... <b>¡Apurate!</b>")
        
        separador3 = QFrame(self)
        separador3.setFrameShape(QFrame.Shape.HLine)
        separador3.setFrameShadow(QFrame.Shadow.Sunken)
        
        linea15 = QLabel("3. Ganá la Partida:")
        linea15.setStyleSheet("""
            color: #8BFF77;
            font-size: 18px;
        """)
        
        linea16 = QLabel("El jugador que gana la partida es quien consigue <u>3 sets completos de propiedades</u>.")
        linea17 = QLabel("Hay <u>distintos tipos de propiedades</u>, rojas, azules, de ferrocarríl, etc.")
        linea18 = QLabel("Cada tipo de propiedad requiere <u>juntar una cierta cantidad del mismo tipo</u>, esto varía.")
        linea19 = QLabel("Ejemplos:")
        linea20 = QLabel("  -  a. Set de propiedades azul completo requiere <b>2 del mismo tipo</b>.")
        linea21 = QLabel("  -  b. Set de propiedades verde completo requiere <b>3 del mismo tipo</b>.")
        linea22 = QLabel("  -  c. Set de propiedades de ferrocarríl (negro) completo requiere <b>4 del mismo tipo</b>.")
        
        separador4 = QFrame(self)
        separador4.setFrameShape(QFrame.Shape.HLine)
        separador4.setFrameShadow(QFrame.Shadow.Sunken)
        
        linea23 = QLabel("4. ¡No Dejés que te Ganen!:")
        linea23.setStyleSheet("""
            color: #FF4B4B;
            font-size: 18px;
        """)
        
        linea24 = QLabel("Jugá cartas de acción contra otros jugadores estratégicamente <u>para evitar que te ganen</u>.")
        linea25 = QLabel("Hay 8 cartas distintas de acción, te permitirán hacerles la vida imposible a los demás.")
        linea26 = QLabel("Robales, intercambiales propiedades, quitales sets completos, hacé que te paguen, y otras cosas más!")
        linea27 = QLabel("Ahora es el momento de ir al apartado de <Ver las Cartas>, ahí vas a ver cuales usar, cómo usarlas y que hacen.")
        
        # ---
        
        self.layout_abajo.addWidget(linea1)
        self.layout_abajo.addSpacing(8)
        self.layout_abajo.addWidget(linea2)
        self.layout_abajo.addSpacing(15)
        self.layout_abajo.addWidget(separador1)
        self.layout_abajo.addWidget(linea3)
        self.layout_abajo.addWidget(linea4)
        self.layout_abajo.addWidget(linea5)
        self.layout_abajo.addWidget(linea6)
        self.layout_abajo.addWidget(linea7)
        self.layout_abajo.addWidget(linea8)
        self.layout_abajo.addWidget(linea9)
        self.layout_abajo.addWidget(linea10)
        self.layout_abajo.addWidget(linea11)
        self.layout_abajo.addSpacing(15)
        self.layout_abajo.addWidget(separador2)
        self.layout_abajo.addWidget(linea12)
        self.layout_abajo.addWidget(linea13)
        self.layout_abajo.addWidget(linea14)
        self.layout_abajo.addSpacing(15)
        self.layout_abajo.addWidget(separador3)
        self.layout_abajo.addWidget(linea15)
        self.layout_abajo.addWidget(linea16)
        self.layout_abajo.addWidget(linea17)
        self.layout_abajo.addWidget(linea18)
        self.layout_abajo.addWidget(linea19)
        self.layout_abajo.addWidget(linea20)
        self.layout_abajo.addWidget(linea21)
        self.layout_abajo.addWidget(linea22)
        self.layout_abajo.addSpacing(15)
        self.layout_abajo.addWidget(separador4)
        self.layout_abajo.addWidget(linea23)
        self.layout_abajo.addWidget(linea24)
        self.layout_abajo.addWidget(linea25)
        self.layout_abajo.addWidget(linea26)
        self.layout_abajo.addWidget(linea27)
        
    def mostrar_ver_cartas(self):
        self.limpiar_layout(self.layout_abajo)
        
    def mostrar_a_cerca_interfaz(self):
        self.limpiar_layout(self.layout_abajo)

    def volver(self):
        self.hide()
    
    def centrar_ventana(self):
        """Método para centrar la ventana en el centro de la pantalla."""
        forma_pantalla = QGuiApplication.primaryScreen().availableGeometry()
        forma_ventana = self.frameGeometry()
        centro_pantalla = forma_pantalla.center()
        forma_ventana.moveCenter(centro_pantalla)
        self.move(forma_ventana.topLeft())