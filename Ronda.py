from abc import abstractmethod
from random import randint

from Jugador import Jugador

class Ronda():
    def __init__(self, numeroRonda:int=1) -> None:
        '''
        Constructor de la clase abstracta Ronda
        
        Args:
        - numeroRonda (int): numero de la ronda. Default = 0
        '''
        
        self.__numeroRonda:int = numeroRonda
        
    def setNumeroRonda(self, numeroRonda:int=1) -> None:
        '''Metodo que setea el numero de la ronda'''
        
        self.__numeroRonda = numeroRonda
        
    def getNumeroRonda(self) -> int:
        '''Metodo que devuelve el numero de la ronda'''
        
        return self.__numeroRonda
    
    def isRondaEspecial(self) -> bool:
        '''Devuelve True si es ronda especial (25%) y False si es ronda normal (75%)'''
        
        if randint(1, 4) == 1:
            return True
        return False
    
    @abstractmethod
    def sumarPuntos(self, jugador:Jugador) -> None:
        '''Metodo abstracto para sumar puntos en los jugadores'''
        
        pass
    
class RondaNormal(Ronda):
    def __init__(self) -> None:
        super().__init__()
        
    def sumarPuntos(self, jugador: Jugador) -> None:
        #jugador.setPuntos(puntos)
        pass
    
class RondaEspecial(Ronda):
    def __init__(self) -> None:
        super().__init__()

    def sumarPuntos(self, jugador: Jugador) -> None:
        #jugador.setPuntos(puntos)
        pass
    
    

    
    
    