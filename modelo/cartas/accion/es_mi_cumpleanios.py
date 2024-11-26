from modelo.cartas.carta import Carta


class EsMiCumpleanios(Carta):
    
    def informacion_para_accion(self) -> str | None:
        return 'EsMiCumpleaños'
    
    def accion(self, info) -> None:
        if self.tipo == 'dinero':
            super().accion()
        else:
            if info[0]:
                cartas = info[0]
                for carta in cartas:
                    carta.duenio.get_objeto_propiedad().quitar_propiedad(carta)
                    carta.duenio = self.duenio
                    self.duenio.agregar_a_banco(carta)
            self.duenio = None
