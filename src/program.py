from src.display import Display
from util.csv import CSValues
from util.gui import Interface

class Program():
    '''Ядро программы'''
    
    def __init__(self):
        
        self.Values = CSValues()
        self.Display = Display(self)
        self.Interface = Interface(self,self.Display)
    
    def main(self):
        '''Основной цикл программы'''
        
        self.Display.root.mainloop()