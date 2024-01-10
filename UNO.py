from Ronda import Ronda
from Jugador import Jugador
from random import choice

class Uno():
    def __init__(self) -> None:
        '''Constructor de la clase'''
        
        self.__cantidadJugadores:int = self.__definirCantidadJugadores()
        self.__losJugadores:list[Jugador] = []
        self.__laRonda:Ronda = Ronda()
        self.__jugadorMezcla:str = ''
        
    def __definirCantidadJugadores(self) -> int:
        '''Metodo que define la cantidad de jugadores que juegan, si la cantidad no es valida vuelve a pedir una cantidad'''
        
        while True:
            try:
                return int(input('Definir cantidad de jugadores: '))
            except ValueError:
                print('La cantidad de jugadores no es válida. Ingresar nuevamente otra cantidad')
    
    def __agregarJugador(self) -> None:
        '''Agrega un nombre de jugador en mayuscula y su posicion, si el nombre del jugador no es valido o el nombre ya se encuentra repetido entre los jugadores vuelve a preguntar el nombre y vacia la lista de jugadores'''
        
        for posicion in range(self.__cantidadJugadores):
            nombreJugador = input('Agregar nombre de jugador/a: ').upper()
            if not nombreJugador.isalpha() or any(
                jugador.getNombre() == nombreJugador for jugador in self.__losJugadores):
                print('El nombre no es valido ingresar nuevamente todos los nombres')
                self.__losJugadores.clear()
                self.__agregarJugador()
            else:
                self.__losJugadores.append(Jugador(nombreJugador))
    
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
    
    def __ganadorMano(self) -> str:
        pass
    
    def __correccion(self) -> None:
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
        self.__quienMezcla()
        self.__sumarRonda()
        self.__sumarRonda()
        self.__sumarRonda()
        self.__sumarRonda()
        self.__sumarRonda()
        
        

def main():
    Uno().jugar()

if __name__ == '__main__':
    main()




