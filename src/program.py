from src.display import Display
from util.csv import CSValues
from util.gui import Interface

import matplotlib.pyplot as plot

class Program():
    '''Ядро программы'''
    
    def __init__(self):
        
        self.Values = CSValues()
        self.Display = Display(self)
        self.Interface = Interface(self,self.Display)
        
        self.Display.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def main(self):
        '''Основной цикл программы'''
        
        self.Display.root.mainloop()
        
    def on_closing(self):
        """Корректное завершение программы: закрыть все графики и выйти."""
        plot.close('all')
        self.Display.root.destroy()