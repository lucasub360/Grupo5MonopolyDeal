from carta.carta import Carta
from jugador import Jugador


class CartaRentaMulticolor(Carta):
    
    @property
    def color(self) -> str:
        if self.color is not str:
            raise ValueError
        return self._color_elegido
    
    def informacion_para_accion(self) -> str | None:
        return 'jugador'
    
    def accion(self, jugador: Jugador, color: str) -> None:
        self.__color_elegido = color
