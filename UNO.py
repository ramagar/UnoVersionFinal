from Ronda import Ronda, RondaNormal, RondaEspecial
from Jugador import Jugador
from random import choice

class Uno():
    def __init__(self) -> None:
        '''Constructor de la clase'''
        self.__cantidadJugadores:int = self.__definirCantidadJugadores()
        self.__losJugadores:list[Jugador] = []
        self.__puntajeJugadorRonda:list[Jugador] = []
        self.__laRonda:Ronda = Ronda()
        self.__jugadorMezcla:str = ''
        
    def __definirCantidadJugadores(self) -> int:
        '''Metodo que define la cantidad de jugadores que juegan, si la cantidad no es valida vuelve a pedir una cantidad'''
        while True:
            try:
                cantidadJugadores = int(input('Definir cantidad de jugadores: '))
                if cantidadJugadores == 1 or cantidadJugadores >= 10:
                    print('La cantidad de jugadores no es válida. Ingresar nuevamente otra cantidad entre 2 y 9')
                else:
                    return cantidadJugadores
            except ValueError:
                print('La cantidad de jugadores no es válida. Ingresar nuevamente otra cantidad')
    
    def __agregarJugador(self) -> None:
        '''Agrega un nombre de jugador en mayuscula y su posicion, si el nombre del jugador no es valido o el nombre ya se encuentra repetido entre los jugadores vuelve a preguntar el nombre y vacia la lista de jugadores'''
        while True:
            i = 0
            while i < self.__cantidadJugadores:
                nombreJugador = input('Agregar nombre de jugador/a: ').upper()
                if not nombreJugador.isalpha() or any(
                    jugador.getNombre() == nombreJugador for jugador in self.__losJugadores):
                    print('El nombre no es valido ingresar nuevamente todos los nombres')
                    self.__losJugadores.clear()
                    i = 0
    
                else:
                    self.__losJugadores.append(Jugador(nombreJugador))
                    i += 1
            break
    
    def __quienMezcla(self) -> str:
        '''Define quien mezcla, la primera mezcla es random'''
        if self.__laRonda == 1:
            self.__jugadorMezcla = choice(self.__losJugadores).getNombre()
        else:
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__jugadorMezcla:
                    if posicion < len(self.__losJugadores) - 1:
                        posicion += 1
                        self.__jugadorMezcla = self.__losJugadores[posicion].getNombre()
                    else:
                        posicion = 0
                        self.__jugadorMezcla = self.__losJugadores[posicion].getNombre()
        return self.__jugadorMezcla
    
    def __sumarRonda(self) -> int:
        '''Define el numero de ronda actual'''
        numeroRonda = self.__laRonda.getNumeroRonda()
        return self.__laRonda.setNumeroRonda(numeroRonda + 1)
    
    def __ganadorMano(self) -> Jugador:
        '''Metodo que pide por input quien fue el ganador de la mano'''
        while True:
            ganador = input('Ingresar quien gano la mano: ').upper()
            for jugador in self.__losJugadores:
                nombreJugador = jugador.getNombre()
                if ganador == nombreJugador.upper():
                    return jugador
                elif ganador in ['CORRECCION', 'CORREGIR', 'ATRAS', 'RECUPERAR']:
                    self.__correccion()
                    break
            print('El jugador proporcionado no se encuentra entre los jugadores')

    def __setPuntosRonda(self) -> None:
        '''Setea los puntos que hizo cada jugador en la ronda'''
        puntajeJugadorRonda:list[Jugador] = self.__losJugadores.copy()
        i = 0
        while i < self.__cantidadJugadores:
            try:
                for jugador in puntajeJugadorRonda:
                    nombreJugador = jugador.getNombre()
                    puntosJugador = int(input(f'Escribir los puntos que hizo {nombreJugador}: '))
                    jugador.setPuntos(nombreJugador, puntosJugador)
                    i += 1
            except ValueError:
                puntajeJugadorRonda:list[Jugador] = self.__losJugadores.copy()
                i = 0
                print('El valor ingresado no es valido, ingresar nuevamente')
        self.__puntajeJugadorRonda = puntajeJugadorRonda
    
    def __sumarPuntos(self) -> None:
        '''Suma los puntos para cada jugador tomando al ganador de la mano y si es ronda especial o normal'''
        ganador = self.__ganadorMano()
        if self.__laRonda.isRondaEspecial():
            for jugador in self.__puntajeJugadorRonda:
                if jugador == ganador:
                    ganador.setPuntosRondaAnterior(ganador.getNombre(), ganador.getPuntos())
                    ganador.setPuntos(ganador.getNombre(), RondaEspecial().sumarPuntos(ganador.getPuntos(), True))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), RondaEspecial().sumarPuntos(jugador.getPuntos()))
        else:
            for jugador in self.__losJugadores:
                if jugador == ganador:
                    ganador.setPuntosRondaAnterior(ganador.getNombre(), ganador.getPuntos())
                    ganador.setPuntos(ganador.getNombre(), RondaNormal().sumarPuntos(ganador.getPuntos(), True))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), RondaNormal().sumarPuntos(jugador.getPuntos()))
         
    
    def __correccion(self) -> None:
        '''Metodo que permite recuperar el puntaje anterior en caso de algun error de tipeo en la sumatoria de puntajes'''
        pass
    
    def __mostrarResultados(self) -> str:
        pass
    
    def __mostrarGrafico(self) -> None:
        pass
    
    def __hayPerdedor(self, perdedor:list[Jugador]) -> None:
        pass
    
    def __guardarResultado(self) -> None:
        pass

    def jugar(self):
        self.__agregarJugador()
        for i in range(3):
            self.__setPuntosRonda()
            self.__sumarPuntos
            for jugador in self.__puntajeJugadorRonda:
                print(f'{jugador.getNombre()} : {jugador.getPuntos()}')
            for jugador in self.__losJugadores:
                print(f'{jugador.getNombre()} : {jugador.getPuntos()}')

        
        

def main():
    Uno().jugar()

if __name__ == '__main__':
    main()




