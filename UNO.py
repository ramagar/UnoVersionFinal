from Ronda import Ronda
from Jugador import Jugador
from random import choice
from os import system

class Uno():
    '''
    Clase que genera el juego de Uno
    
    Atributos:
    - __laApuesta (str): Define que es lo que se apuesta
    - __cantidadJugadores (int): Cantidad de jugadores que juegan
    - __losJugadores (list[Jugador]): Lista de los jugadores, con su nombre y sus puntos
    - __ganadorRonda (str): Nombre del jugador que gano la ronda
    - __puntajesJugadoresRonda (list[int|float]): Lista de puntajes que hizo cada jugador en la ronda
    - __laRonda (Ronda): Ronda actual en la que se esta jugando
    - __jugadorMezcla (str): Nombre del jugador al que le toca mezclar en la ronda acutal
    '''
    def __init__(self) -> None:
        '''Constructor de la clase Uno'''
        self.__laApuesta:str = str()
        self.__cantidadJugadores:int = int()
        self.__losJugadores:list[Jugador] = []
        self.__ganadorRonda:str = str()
        self.__puntajesJugadoresRonda:list[float|int] = []
        self.__laRonda:Ronda = Ronda()
        self.__jugadorMezcla:str = str()
    
    def __setApuesta(self) -> None:
        '''Metodo que define la apuesta por la que se juega'''
        system('cls')
        self.__laApuesta = input('Escribir que es lo que se apuesta: ')
        system('cls')
        
    def __setCantidadJugadores(self) -> None:
        '''Metodo que define la cantidad de jugadores que juegan. Si la cantidad no es valida vuelve a pedir una cantidad'''
        while True:
            try:
                cantidadJugadores = int(input('Definir cantidad de jugadores: '))
                print('\n')
                if cantidadJugadores > 1 and cantidadJugadores < 10:
                    self.__cantidadJugadores = cantidadJugadores
                    system('cls')
                    break
                else:
                    system('cls')
                    print('La cantidad de jugadores no es válida. Ingresar nuevamente otra cantidad entre 2 y 9\n\n')
            except ValueError:
                system('cls')
                print('La cantidad de jugadores no es válida. Ingresar nuevamente otra cantidad\n\n')
    
    def __agregarJugador(self) -> None:
        '''Agrega un nombre de jugador en mayuscula. Si el nombre del jugador no es valido o el nombre ya se encuentra repetido entre los jugadores, vacia la lista de jugadores y vuelve a preguntar los nombres de cada uno de los jugadores'''
        while True:
            i = 0
            while i < self.__cantidadJugadores:
                nombreJugador = input(f'Agregar nombre de jugador {i+1}: ').upper()
                print('')
                if not nombreJugador.isalpha() or any(
                    jugador.getNombre() == nombreJugador for jugador in self.__losJugadores):
                    system('cls')
                    print('El nombre no es valido ingresar nuevamente todos los nombres\n\n')
                    self.__losJugadores.clear()
                    i = 0
                else:
                    self.__losJugadores.append(Jugador(nombreJugador))
                    i += 1
            system('cls')
            break
    
    def __setQuienMezcla(self) -> None:
        '''Metodo que define el nombre del jugador al que le toca mezclar. El primer jugador que mezcla se define al azar'''
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
        print(f'Le toca mezclar a {self.__jugadorMezcla}\n\n')
    
    def __setRonda(self) -> None:
        '''Metodo que define el numero de ronda actual'''
        print(f'Es la ronda numero {self.__laRonda.getNumeroRonda()}\n\n')
        self.__laRonda.setNumeroRonda(self.__laRonda.getNumeroRonda() + 1)
        self.__laRonda.setRondaEspecial()
        if self.__laRonda.getRondaEspecial():
            print('-------------------\nHAY RONDA ESPECIAL!\n-------------------\n\n')
    
    def __setGanadorRonda(self) -> None:
        '''Metodo que define el nombre del jugador que gano la ronda'''
        while True:
            correccion = False
            ganador = input('Ingresar quien gano la mano: ').upper()
            print('')
            for jugador in self.__losJugadores:
                if ganador == jugador.getNombre().upper():
                    self.__ganadorRonda = ganador
                    return None
                elif ganador in ['CORRECCION', 'CORREGIR', 'ATRAS', 'RECUPERAR']:
                    self.__correccion()
                    correccion = True
                    break
            if not correccion:
                print('\nEl jugador proporcionado no se encuentra entre los jugadores\n\n')

    def __setPuntosRonda(self) -> None:
        '''Metodo que define los puntos que se hicieron en la ronda'''
        self.__puntajesJugadoresRonda.clear()
        while True:
            i = 0
            while i < len(self.__losJugadores):
                for jugador in self.__losJugadores:
                    try:
                        if jugador.getNombre() != self.__ganadorRonda:
                            self.__puntajesJugadoresRonda.append(int(input(f'Escribir cuantos puntos hizo {jugador.getNombre()}: ')))
                            print('')
                        else:
                            self.__puntajesJugadoresRonda.append(0)
                        i += 1
                    except ValueError:
                        self.__puntajesJugadoresRonda.clear()
                        print('\n\nEl valor no es valido, volver a escribir los puntajes\n\n')
                        i = 0
                        break
            print('\n'*10)
            break        
    
    def __setPuntos(self) -> None:
        '''Metodo que define los puntos para cada jugador tomando al ganador de la mano y los puntos de la ronda anterior de cada jugador'''
        if self.__laRonda.getRondaEspecial():
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__ganadorRonda:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), round(self.__sumarPuntosRondaEspecial(self.__puntajesJugadoresRonda, posicion, True), 2))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), round(self.__sumarPuntosRondaEspecial(self.__puntajesJugadoresRonda, posicion),2))
        else:
            for posicion, jugador in enumerate(self.__losJugadores):
                if jugador.getNombre() == self.__ganadorRonda:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), round(self.__sumarPuntosRondaNormal(self.__puntajesJugadoresRonda, posicion,  True), 2))
                else:
                    jugador.setPuntosRondaAnterior(jugador.getNombre(), jugador.getPuntos())
                    jugador.setPuntos(jugador.getNombre(), round(self.__sumarPuntosRondaNormal(self.__puntajesJugadoresRonda, posicion), 2))
    
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
        '''Metodo que define el puntaje maximo y minimo en donde el jugador pierde. Si un jugador alcanza alguno de esos puntajes se define un perdedor y se termina el juego'''
        maximo = self.__cantidadJugadores * 100
        minimo = self.__cantidadJugadores * (-75)
        for jugador in self.__losJugadores:
            if jugador.getPuntos() > maximo or jugador.getPuntos() < minimo:
                system('cls')
                print('Hay un perdedor/a en la sala...', '\n')
                input('Toca ENTER para ver quien es: ')
                system('cls')
                for jugador in self.__losJugadores:
                    if jugador.getPuntos() == min([perdedor.getPuntos() for perdedor in self.__losJugadores]):
                        print(f'El perdedor/a es {jugador.getNombre()} y tiene que {self.__laApuesta}\n\n\n')
                        return True
        return False
    
    def __mostrarResultados(self) -> None:
        '''Metodo para mostar los resultados por consola'''
        print('     Nombre     |     Puntos     \n', '~'*33, sep='')
        for jugador in self.__losJugadores:
            print(f'{jugador.getNombre()}'.center(16), '|', f'{jugador.getPuntos()}'.center(16), sep='')
        print('~'*33, '\n\n')
    
    def __mostrarGrafico(self) -> None:
        pass
    
    def __guardarResultado(self) -> None:
        input('Toca Enter para terminar el juego: ')

    def jugar(self):
        '''Metodo para jugar al Uno'''
        self.__setApuesta()
        self.__setCantidadJugadores()
        self.__agregarJugador()
        while not self.__hayPerdedor():
            self.__setQuienMezcla()
            self.__setRonda()
            self.__setGanadorRonda()
            self.__setPuntosRonda()
            self.__setPuntos()
            self.__mostrarResultados()
            self.__mostrarGrafico()
        self.__mostrarResultados()
        self.__mostrarGrafico()
        self.__guardarResultado()

def main():
    '''Funcion que inicializa el juego y lo termina una vez que se determina un perdedor'''
    Uno().jugar()
    
if __name__ == '__main__':
    main()