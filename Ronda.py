from random import randint

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
    
    

    
    
    