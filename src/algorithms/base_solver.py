from abc import ABC,abstractmethod

class BaseSolver(ABC):
    @abstractmethod
    def solve(self,init_state:tuple):
        
        pass