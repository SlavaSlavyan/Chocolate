import tkinter
from tkinter import ttk

from util.gui import Interface

class Display:
    '''Класс Отображения'''
    
    def __init__(self, mainself):
        
        self.create_window()
        self.set_style()
        
        self.data_frame = None 
        self.file_frame = None
        self.graph_frame = None
        self.status = None
    
    def create_window(self):
        '''создание экземпляра окна'''
        
        self.root = tkinter.Tk()
        self.root.title("Chockolate Analisator SlavaSlavyan (CASLL)")
        self.root.geometry("1200x800")
        
    def set_style(self):
        '''задаём общий стиль программы'''
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', font=('Arial', 10))
        
    