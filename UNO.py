from Ronda import Ronda
from Jugador import Jugador
from random import choice

class Uno():
    def __init__(self) -> None:
        '''Constructor de la clase'''
        self.__laApuesta:str = str()
        self.__cantidadJugadores:int = int()
        self.__losJugadores:list[Jugador] = []
        self.__ganadorRonda:str = str()
        self.__puntajesJugadoresRonda:list[float|int] = []
        self.__laRonda:Ronda = Ronda()
        self.__jugadorMezcla:str = str()
    
    def __setApuesta(self) -> None:
        '''Metodo que setea la apuesta por la que se juega'''
        self.__laApuesta = input('Escribir que es lo que se apuesta: ')
        
    def __setCantidadJugadores(self) -> None:
        '''Metodo que define la cantidad de jugadores que juegan, si la cantidad no es valida vuelve a pedir una cantidad'''
        while True:
            try:
                cantidadJugadores = int(input('Definir cantidad de jugadores: '))
                if cantidadJugadores > 1 and cantidadJugadores < 10:
                    self.__cantidadJugadores = cantidadJugadores
                    break
                else:
                    print('La cantidad de jugadores no es válida. Ingresar nuevamente otra cantidad entre 2 y 9')
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
    
    def __quienMezcla(self) -> None:
        '''Define quien mezcla, la primera mezcla es random'''
        if self.__laRonda.getNumeroRonda() == 1:
            self.__jugadorMezcla = choice(self.__losJugadores).getNombre()
        else:
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__jugadorMezcla:
                    if posicion < len(self.__losJugadores) - 1:
                        posicion += 1
                        self.__jugadorMezcla = self.__losJugadores[posicion].getNombre()
                        break
                    else:
                        posicion = 0
                        self.__jugadorMezcla = self.__losJugadores[posicion].getNombre()
                        break
        print(f'Le toca mezclar a {self.__jugadorMezcla}')
    
    def __sumarRonda(self) -> None:
        '''Define el numero de ronda actual'''
        print(f'Es la ronda numero {self.__laRonda.getNumeroRonda()}')
        self.__laRonda.setNumeroRonda(self.__laRonda.getNumeroRonda() + 1)
    
    def __ganadorMano(self) -> None:
        '''Metodo que pide por input quien fue el ganador de la mano y lo guarda como ganador ronda'''
        while True:
            correccion = False
            ganador = input('Ingresar quien gano la mano: ').upper()
            for jugador in self.__losJugadores:
                if ganador == jugador.getNombre().upper():
                    self.__ganadorRonda = ganador
                    return None
                elif ganador in ['CORRECCION', 'CORREGIR', 'ATRAS', 'RECUPERAR']:
                    self.__correccion()
                    correccion = True
                    break
            if not correccion:
                print('El jugador proporcionado no se encuentra entre los jugadores')


    def __setPuntosRonda(self) -> None:
        '''Setea los puntos que hizo cada jugador en la ronda'''
        self.__puntajesJugadoresRonda.clear()
        while True:
            i = 0
            while i < len(self.__losJugadores):
                for jugador in self.__losJugadores:
                    try:
                        if jugador.getNombre() != self.__ganadorRonda:
                            self.__puntajesJugadoresRonda.append(int(input(f'Escribir cuantos puntos hizo {jugador.getNombre()}: ')))
                        else:
                            self.__puntajesJugadoresRonda.append(0)
                        i += 1
                    except ValueError:
                        self.__puntajesJugadoresRonda.clear()
                        print('El valor no es valido, volver a escribir los puntajes')
                        i = 0
                        break
            break        
    
    def __sumarPuntos(self) -> None:
        '''Suma los puntos para cada jugador tomando al ganador de la mano y si es ronda especial o normal'''
        if self.__laRonda.isRondaEspecial():
            print('FUE RONDA ESPECIAL')
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__ganadorRonda:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaEspecial(self.__puntajesJugadoresRonda, posicion, True))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaEspecial(self.__puntajesJugadoresRonda, posicion))
        else:
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__ganadorRonda:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaNormal(self.__puntajesJugadoresRonda, posicion,  True))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), self.__sumarPuntosRondaNormal(self.__puntajesJugadoresRonda, posicion))
    
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
        print('Se activo el modo de correccion')
        for jugador in self.__losJugadores:
            jugador.setPuntos(jugador.getNombre(), jugador.getPuntosRondaAnterior())
            print(f'{jugador.getNombre()} : {jugador.getPuntos()}')
    
    def __hayPerdedor(self) -> bool:
        '''Define el puntaje maximo y minimo en donde el jugador pierde y si alcanza alguno de esos puntajes pierde y termina el juego'''
        maximo = self.__cantidadJugadores * 100
        minimo = self.__cantidadJugadores * (-75)
        for jugador in self.__losJugadores:
            if jugador.getPuntos() > maximo or jugador.getPuntos() < minimo:
                print('Hay un perdedor/a en la sala...', '\n')
                input('Toca ENTER para ver quien es: ')
                for jugador in self.__losJugadores:
                    if jugador.getPuntos() == min([perdedor.getPuntos() for perdedor in self.__losJugadores]):
                        print(f'El perdedor/a es {jugador.getNombre()} y tiene que {self.__laApuesta}')
                        return True
        return False
    
    def __mostrarResultados(self) -> str:
        pass
    
    def __mostrarGrafico(self) -> None:
        pass
    
    def __guardarResultado(self) -> None:
        pass

    def jugar(self):
        self.__setApuesta()
        self.__setCantidadJugadores()
        self.__agregarJugador()
        while not self.__hayPerdedor():
            self.__quienMezcla()
            self.__sumarRonda()
            self.__ganadorMano()
            self.__setPuntosRonda()
            self.__sumarPuntos()
            for jugador in self.__losJugadores:
                print(f'{jugador.getNombre()} : {jugador.getPuntosRondaAnterior()} | {jugador.getPuntos()}')

        
        

def main():
    Uno().jugar()

if __name__ == '__main__':
    main()




