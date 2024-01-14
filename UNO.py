from Ronda import Ronda
from Jugador import Jugador
from random import choice, random
import matplotlib.pyplot as plt
from os import system, getcwd, chdir
import csv

RUTA = getcwd()

class Uno():
    '''
    Clase que genera el juego de Uno
    
    Atributos:
    - __laApuesta (str): Que es lo que se apuesta
    - __cantidadJugadores (int): Cantidad de jugadores que juegan
    - __losJugadores (list[Jugador]): Lista de los jugadores, con su nombre y sus puntos
    - __ganadorRonda (str): Nombre del jugador que gano la ronda
    - __puntajesJugadoresRonda (list[int|float]): Lista de puntajes que hizo cada jugador en la ronda
    - __laRonda (Ronda): Ronda actual en la que se esta jugando
    - __jugadorMezcla (str): Nombre del jugador al que le toca mezclar en la ronda acutal
    - __puntajeMaximo (int): Puntaje maximo en donde si un jugador lo alcanza se termina el juego
    - __puntajeMinimo (int): Puntaje minimo en donde si un jugador lo alcanza se termina el juego
    - __elPerdedor (str): Nombre del jugador que perdio el juego
    '''
    
    def __init__(self) -> None:
        '''Constructor de la clase Uno'''
        
        self.__laApuesta:str = str()
        '''Que es lo que se apuesta'''
        self.__cantidadJugadores:int = int()
        '''Cantidad de jugadores que juegan'''
        self.__losJugadores:list[Jugador] = []
        '''Lista de los jugadores, con su nombre y sus puntos'''
        self.__ganadorRonda:str = str()
        '''Nombre del jugador que gano la ronda'''
        self.__puntajesJugadoresRonda:list[float|int] = []
        '''Lista de puntajes que hizo cada jugador en la ronda'''
        self.__laRonda:Ronda = Ronda()
        '''Ronda actual en la que se esta jugando'''
        self.__jugadorMezcla:str = str()
        '''Nombre del jugador al que le toca mezclar en la ronda acutal'''
        self.__puntajeMaximo:int = int()
        '''Puntaje maximo en donde si un jugador lo alcanza se termina el juego'''
        self.__puntajeMinimo:int = int()
        '''Puntaje minimo en donde si un jugador lo alcanza se termina el juego'''
        self.__coloresJugadores:list[float] = []
        '''Lista de colores asignados a cada jugador'''
        self.__elPerdedor:str = str()
        '''Nombre del jugador que perdio el juego'''
    
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
    
    def __setPuntajeMaximoMinimo(self) -> None:
        '''Metodo que define el puntaje maximo y minimo al que puede llegar un jugador para que termine el juego'''
        self.__puntajeMaximo = self.__cantidadJugadores * 100
        self.__puntajeMinimo = self.__cantidadJugadores * (-75)
    
    def __agregarJugador(self) -> None:
        '''Metodo que agrega un nombre de jugador en mayuscula. Si el nombre del jugador no es valido o el nombre ya se encuentra repetido entre los jugadores, vuelve a preguntar los nombres de cada uno de los jugadores'''
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
        '''Metodo que define los puntos actuales y los puntos de la ronda anterior para cada jugador'''
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
        '''Metodo que suma los puntos de los jugadores durante la ronda normal'''
        if isGanador:
            return self.__losJugadores[posicion].getPuntos() + sum([puntos for puntos in listaPuntos])
        else:
            return self.__losJugadores[posicion].getPuntos() - listaPuntos[posicion]/2
        
    def __sumarPuntosRondaEspecial(self, listaPuntos:list[float|int], posicion:int, isGanador:bool=False) -> int|float:
        '''Metodo que suma los puntos de los jugadores durante la ronda especial'''
        if isGanador:
            return self.__losJugadores[posicion].getPuntos() + sum([puntos for puntos in listaPuntos]) * 1.2
        else:
            return self.__losJugadores[posicion].getPuntos() - listaPuntos[posicion]
    
    def __correccion(self) -> None:
        '''Metodo que permite recuperar el puntaje anterior en caso de algun error de tipeo en la sumatoria de puntajes'''
        print('\n\nSe activo el modo de correccion\n\n')
        for jugador in self.__losJugadores:
            jugador.setPuntos(jugador.getNombre(), jugador.getPuntosRondaAnterior())
            print(f'{jugador.getNombre()} : {jugador.getPuntos()}')
    
    def __hayPerdedor(self) -> bool:
        '''Metodo que devuelve True si hay un perdedor y False si no lo hay. El perdedor se define si algun jugador llega al puntaje maximo o al puntaje minimo'''
        for jugador in self.__losJugadores:
            if jugador.getPuntos() > self.__puntajeMaximo or jugador.getPuntos() < self.__puntajeMinimo:
                system('cls')
                print('Hay un perdedor/a en la sala...', '\n')
                input('Toca ENTER para ver quien es: ')
                system('cls')
                for jugador in self.__losJugadores:
                    if jugador.getPuntos() == min([perdedor.getPuntos() for perdedor in self.__losJugadores]):
                        self.__elPerdedor = jugador.getNombre()
                        print(f'El perdedor/a es {self.__elPerdedor} y tiene que {self.__laApuesta}\n\n\n')
                        return True
        return False
    
    def __mostrarResultados(self) -> None:
        '''Metodo para mostar los resultados por consola'''
        print('     Nombre     |     Puntos     \n', '~'*33, sep='')
        for jugador in self.__losJugadores:
            print(f'{jugador.getNombre()}'.center(16), '|', f'{jugador.getPuntos()}'.center(16), sep='')
        print('~'*33, '\n\n')
    
    def __mostrarGrafico(self) -> None:
        '''Metodo que muestra el grafico de los puntajes'''
        if self.__laRonda.getNumeroRonda() == 2:
            self.__coloresJugadores = [(random(), random(), random()) for _ in range(self.__cantidadJugadores)]
        fig, ax = plt.subplots(figsize=(8.5, 10))
        ax.set_ylim(self.__puntajeMinimo, self.__puntajeMaximo)
        ax.bar([jugador.getNombre() for jugador in self.__losJugadores], [jugador.getPuntos() for jugador in self.__losJugadores], label=[jugador.getNombre() for jugador in self.__losJugadores], color= self.__coloresJugadores)
        ax.set_ylabel('Puntos')
        ax.set_title(f'RONDA {self.__laRonda.getNumeroRonda()-1}')
        ax.legend(title='Jugadores')
        plt.show(block=False)
    
    def __guardarResultado(self) -> None:
        '''Metodo que guarda los resultados en un excel dentro de la carpeta de ejecucion'''
        chdir(RUTA)
        with open('resultados.csv', 'a', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([f'{self.__elPerdedor} =====> {self.__laApuesta}'])
        input('Toca Enter para terminar el juego')

    def jugar(self):
        '''Metodo para jugar al Uno'''
        self.__setApuesta()
        self.__setCantidadJugadores()
        self.__setPuntajeMaximoMinimo()
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
        self.__guardarResultado()

def main():
    '''Funcion que inicializa el juego y lo termina una vez que se determina un perdedor'''
    Uno().jugar()
    
if __name__ == '__main__':
    main()