class Jugador():
    def __init__(self, nombre:str, puntos:int|float=0) -> None:
        '''
        Contructor de la clase Jugador
        
        Args:
        - nombre (str): el nombre del jugador
        - puntos (float): los puntos del jugador. Default = 0
        '''
        
        self.__jugador:dict = {nombre:puntos}
         
    def setPuntos(self, nombre:str, puntos:int=0) -> None:
        '''Metodo que setea los puntos del jugador'''
        
        self.__jugador = {nombre:puntos}
        
    def getPuntos(self) -> float:
        '''Metodo que devuelve los puntos del jugador'''
        
        return list(self.__jugador.values())[0]
    
    def getNombre(self) -> str:
        '''Metodo que devuelve el nombre del jugador'''
        
        return list(self.__jugador.keys())[0]
    
    