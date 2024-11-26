import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QFontDatabase
from vistas.vista_main_menu import MainMenu

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Fuente personalizada:
    font_id = QFontDatabase.addApplicationFont("imagenes/ui/OMDFMP+KabelMediumITC.ttf")
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app_font = QFont(font_family)
    app_font.setPointSize(12) # <-- Tamaño de la fuente.
    app.setFont(app_font)     # <-- Aplicar la fuente a toda la aplicación.

    # Inicializar la ventana principal:
    try:
        main_window = MainMenu()
        main_window.show()
    except Exception as e:
        print(f"\n(¡Error!): No se pudo inicializar el programa: {e}\n")
        sys.exit(1)

    sys.exit(app.exec())