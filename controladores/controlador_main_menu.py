from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtMultimedia import QMediaPlayer
from crear_partida import CrearPartida
from vistas.vista_como_juego import ComoJuego
from vistas.vista_opciones import Opciones
from vistas.vista_estadisticas import Estadisticas

class controlador_main_menu (QMainWindow):
    def __init__(self): 
        super().__init__()
        
        self.player = QMediaPlayer()
        
        # Funciones de los botones:
        self.boton_crear_partida=CrearPartida(self)
        self.boton_opciones=Opciones(self)
        self.boton_como_juego=ComoJuego(self)
        self.boton_estadisticas=Estadisticas(self)
    
    # Sonido de los botones:
    def sonido_click(self):
        self.player.stop()
        self.player.play()
    
    # Botón crear partida:
    def mostrar_crear_partida(self):
        self.sonido_click()
        self.hide()
        self.boton_crear_partida.exec()
    
    # Botón opciones:
    def mostrar_opciones(self):
        self.sonido_click()
        self.hide()
        self.boton_opciones.exec()
        
    # Botón cómo jugar:
    def mostrar_como_juego(self):
        self.sonido_click()
        self.hide()
        self.boton_como_juego.exec()
    
    # Botón estadísticas:
    def mostrar_estadisticas_inicio_sesion(self):
        self.sonido_click()
        self.hide()
        self.boton_estadisticas.exec()
