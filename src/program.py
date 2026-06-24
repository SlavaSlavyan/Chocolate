from src.display import Display

class Program():
    '''Ядро программы'''
    
    def __init__(self):
        
        self.Display = Display(self)
    
    def main(self):
        '''Основной цикл программы'''
        
        self.Display.root.mainloop()