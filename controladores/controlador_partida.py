from random import choice
from modelo.jugador import Jugador
from modelo.mazo_de_cartas import MazoDeCartas
from modelo.mazo_de_descarte import MazoDeDescarte
from modelo.cartas.carta import Carta
from modelo.base_de_datos.conexion.monopoly_db import Database
from modelo.base_de_datos.partida_dao.partida_bdd import PartidaBDD
from modelo.base_de_datos.partida_dao.partida_dao_imp import PartidaDaoImpl
# from vistas. #tiene que ir la vista de la partida


class ControladorPartida:
    def __init__(self, jugadores: list[Jugador]):
        self.__vista = Vista(self) # poner el nombre de la vista correcto
        self.__jugadores = jugadores  # Instancias de la clase Jugador
        self.__jugador_actual = choice(self.__jugadores)
        self.__cartas_jugadas_en_turno = 0
        self.__mazo = MazoDeCartas()
        self.__cartas_descarte = MazoDeDescarte()  # Pila de descarte
        self.__turno_actual = 0
        self.__ganador: Jugador = None
        self.repartir_cartas()
        self.__vista.show()

    # Reparte 5 cartas a cada jugador
    def repartir_cartas(self):
        for jugador in self.__jugadores:
            jugador.tomar_carta(self.__mazo.dar_cartas(5))
    
    # Toma una carta aleartoria del mazo eliminandola
    def tomar_carta_mazo(self,jugador: Jugador):
        jugador.tomar_carta(self.__mazo.dar_cartas(1))
    
############################################################################################################################
######################################## Código para jugar las cartas ######################################################
############################################################################################################################

    def jugar_carta(self, carta: Carta) -> None:
        # Verificar si la carta puede ser jugada
        pedido = carta.informacion_para_accion()
        if pedido is not None:
            datos_para_accion = self.procesa_pedido(pedido, carta)
            carta.accion(datos_para_accion)
        else:
            carta.accion()
        if self.chequea_ganador():
            self.fin_de_partida()
        self.__cartas_jugadas_en_turno += 1
        if self.__cartas_jugadas_en_turno == 3:
            self.terminar_turno()
    
    def procesa_pedido(self, pedido, carta: Carta) -> list:
        if pedido == 'EsMiCumpleaños':
            return self.pedido_es_mi_cumpleanios(carta)
        elif pedido == 'CobradordDeDeuda':
            return self.pedido_cobrador_de_deuda(carta)
        elif pedido == 'NegocioFurtivo':
            return self.pedido_negocio_furtivo(carta)
        elif pedido == 'PasaPorLaSalida':
            return [self.__mazo]
        elif pedido == 'TratoForzoso':
            return self.pedido_trato_forzoso(carta)
        elif pedido == 'Renta':
            return self.pedido_renta(carta)
        elif pedido == 'RentaMulticolor':
            return self.pedido_renta_multicolor(carta)
        elif pedido == 'PropiedadComodin':
            return [self.elegir_color(carta)]
        else:
            raise ValueError
    
    def pedido_es_mi_cumpleanios(self, carta: Carta) -> list[Carta]:
        cartas_para_pago = []
        jugadores_validos = self.jugadores_validos_para_cobro(2)
        for jugador in jugadores_validos:
            if jugador is not carta.duenio:
                cartas_para_pago.extend(self.elegir_dinero(jugador, 2))
        return cartas_para_pago
    
    def pedido_cobrador_de_deuda(self, carta: Carta) -> list[Carta]:
        cartas_para_pago = []
        jugadores_validos = self.jugadores_validos_para_cobro(5)
        jugador_seleccionado = self.elegir_jugador(carta.duenio, jugadores_validos)
        cartas_para_pago = self.elegir_dinero(jugador_seleccionado, 5)
        return cartas_para_pago
    
    def pedido_negocio_furtivo(self, carta: Carta) -> list[Carta]:
        propiedad_seleccionada = []
        jugador_seleccionado = self.elegir_jugador(carta.duenio, self.__jugadores)
        propiedad_seleccionada = self.elegir_propiedad(jugador_seleccionado) # hay que verificar que no esté en un set
        return [propiedad_seleccionada]

    def pedido_trato_forzoso(self, carta: Carta) -> list[Carta]:
        propiedad_propia = self.elegir_propiedad(carta.duenio) # se podría mandar una cadena que se muestre en el dialog
        jugador_seleccionado = self.elegir_jugador(carta.duenio) # ej. 'Elija una de sus propiedades para intercambiar con otro jugador'
        propiedad_otro = self.elegir_propiedad(jugador_seleccionado) # Esta cadena se mostraría en el dialog en la interfaz
        return [propiedad_propia, propiedad_otro]

    def pedido_renta(self, carta: Carta) -> list[Carta]:
        cartas_para_pago = []
        color = self.elegir_color(carta.color)
        cantidad_a_cobrar = carta.duenio.get_objeto_propiedad().get_valor_alquiler(color)
        jugadores_validos = self.jugadores_validos_para_cobro(cantidad_a_cobrar)
        for jugador in jugadores_validos:
            if jugador is not carta.duenio:
                cartas_para_pago.extend(self.elegir_dinero(jugador, cantidad_a_cobrar))
        return cartas_para_pago

    def pedido_renta_multicolor(self, carta: Carta) -> list[Carta]:
        cartas_para_pago = []
        color = self.elegir_color(carta.color)
        cantidad_a_cobrar = carta.duenio.get_objeto_propiedad().get_valor_alquiler(color)
        jugadores_validos = self.jugadores_validos_para_cobro(cantidad_a_cobrar)
        jugador_elegido = self.elegir_jugador(carta.duenio, jugadores_validos)
        cartas_para_pago.extend(self.elegir_dinero(jugador_elegido, cantidad_a_cobrar))
        return cartas_para_pago
    
    def jugadores_validos_para_cobro(self, valor_minimo: int):
        return [jugador for jugador in self.__jugadores if jugador.calcular_valor_banco_propiedades() > valor_minimo]

    def elegir_jugador(self, jugador_excluido: Jugador, jugadores_validos: list[Jugador]) -> Jugador:
        jugadores = []
        for jugador in jugadores_validos:
            if jugador is not jugador_excluido:
                jugadores.append(jugador)
        dialogo = self.__vista.dialog_pedir_jugador(jugadores)
        dialogo.exec()
        return dialogo.jugador_seleccionado

    def elegir_dinero(self, jugador_seleccionado: Jugador, dinero_necesario: int) -> list[Carta]:
        dialogo = self.__vista.dialog_pedir_dinero(jugador_seleccionado.get_banco(), dinero_necesario)
        dialogo.exec()
        return dialogo.cartas_seleccionadas

    def elegir_propiedad(self, jugador: Jugador):
        propiedades = jugador.get_objeto_propiedad().get_cartas_propiedades()
        dialogo = self.__vista.dialog_pedir_propiedad(propiedades)
        dialogo.exec()
        return dialogo.propiedad_seleccionada
    
    def elegir_color(self, carta: Carta) -> str:
        lista_colores = carta.color
        dialogo = self.__vista.dialog_pedir_color(lista_colores)
        dialogo.exec()
        return dialogo.color_seleccionado

############################################################################################################################
######################################## Termina código para jugar las cartas ##############################################
############################################################################################################################

############################################################################################################################
############################################# Código para terminar la partida ##############################################
############################################################################################################################

    def chequea_ganador(self) -> bool:
        for jugador in self.__jugadores:
            sets_jugador = jugador.get_objeto_propiedad().get_sets_completos()
            if len(sets_jugador) == 3:
                if self.__ganador is None:
                    self.__ganador = jugador
                elif isinstance(self.__ganador, Jugador):
                    self.__ganador = [self.__ganador]
                    self.__ganador.append(jugador)
                    break
        if self.__ganador is not None:
            return True
        return False
    
    def fin_de_partida(self):
        conexion = Database().conexion()
        partida_dao = PartidaDaoImpl(conexion)
        partida = PartidaBDD()
        partida.id_partida = partida_dao.obtener_id_partida()
        if isinstance(self.__ganador, Jugador):
            partida.id_ganador = self.__ganador.datos_bdd.get_id_jugador()
        else:
            partida.id_ganador = None
        partida_dao.agregar_partida(partida)
        for jugador in self.__jugadores:
            if jugador.datos_bdd is not None:
                partida_dao.registrar_jugador_en_partida(partida, jugador)
        conexion.close()
        self.__vista.finalizar_partida()
                
############################################################################################################################
########################################### Termina código para ganar la partida ###########################################
############################################################################################################################

    def terminar_turno(self):
        pass
    
    #devulve el jugador actual segun el turno actual
    def jugador_actual(self):
        return self.__jugadores[self.__turno_actual]
    
    #devuelve el turno actual segun la posicion de la lista de jugadores
    def pasar_turno(self):
        if self.turno_actual + 1 >= len(self.__jugadores): 
            self.turno_actual = 0
        else: self.turno_actual += 1
