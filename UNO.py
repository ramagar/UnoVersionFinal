from Ronda import Ronda
from Jugador import Jugador
from random import choice

class Uno():
    def __init__(self) -> None:
        '''Constructor de la clase'''
        self.__cantidadJugadores:int = self.__definirCantidadJugadores()
        self.__losJugadores:list[Jugador] = []
        self.__ganadorRonda:str = ''
        self.__puntajeJugadoresRonda:list[float|int] = []
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
    
    def __ganadorMano(self) -> None:
        '''Metodo que pide por input quien fue el ganador de la mano y lo guarda como ganador ronda'''
        while True:
            ganador = input('Ingresar quien gano la mano: ').upper()
            for jugador in self.__losJugadores:
                if ganador == jugador.getNombre().upper():
                    self.__ganadorRonda = ganador
                    return None
                elif ganador in ['CORRECCION', 'CORREGIR', 'ATRAS', 'RECUPERAR']:
                    self.__correccion()
                    return None
            print('El jugador proporcionado no se encuentra entre los jugadores')

    def __setPuntosRonda(self) -> None:
        '''Setea los puntos que hizo cada jugador en la ronda'''
        self.__puntajeJugadoresRonda.clear()
        while True:
            i = 0
            while i < len(self.__losJugadores):
                for jugador in self.__losJugadores:
                    try:
                        if jugador.getNombre() != self.__ganadorRonda:
                            self.__puntajeJugadoresRonda.append(int(input(f'Escribir cuantos puntos hizo {jugador.getNombre()}: ')))
                        else:
                            self.__puntajeJugadoresRonda.append(0)
                        i += 1
                    except ValueError:
                        self.__puntajeJugadoresRonda.clear()
                        print('El valor no es valido, volver a escribir los puntajes')
                        break
            break
    
    def __sumarPuntos(self) -> None:
        '''Suma los puntos para cada jugador tomando al ganador de la mano y si es ronda especial o normal'''
        if self.__laRonda.isRondaEspecial():
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__ganadorRonda:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaEspecial(self.__puntajeJugadoresRonda, posicion, True))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaEspecial(self.__puntajeJugadoresRonda, posicion))
        else:
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__ganadorRonda:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaNormal(self.__puntajeJugadoresRonda, posicion,  True))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaNormal(self.__puntajeJugadoresRonda, posicion))
    
    def __sumarPuntosRondaNormal(self, listaPuntos:list[float|int], posicion:int, isGanador:bool=False) -> int|float:
        '''Metodo logico para sumar puntos en los jugadores durante la ronda normal'''
        if isGanador:
            return self.__losJugadores[posicion].getPuntos() + sum([puntos for puntos in listaPuntos])
        else:
            return self.__losJugadores[posicion].getPuntos() - listaPuntos[posicion]/2
        
    def __sumarPuntosRondaEspecial(self, listaPuntos:list[float|int], posicion:int, isGanador:bool=False) -> int|float:
        '''Metodo logico para sumar puntos en los jugadores durante la ronda especial'''
        if isGanador:
            return self.__losJugadores[posicion].getPuntos() + sum([puntos for puntos in listaPuntos]) * 1.2
        else:
            return self.__losJugadores[posicion].getPuntos() - listaPuntos[posicion]
    
    
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
            self.__ganadorMano()
            self.__setPuntosRonda()
            self.__sumarPuntos()
            for puntaje in self.__puntajeJugadoresRonda:
                print(puntaje)
            for jugador in self.__losJugadores:
                print(f'{jugador.getNombre()} : {jugador.getPuntosRondaAnterior()} | {jugador.getPuntos()}')

        
        

def main():
    Uno().jugar()

if __name__ == '__main__':
    main()




