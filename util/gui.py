import tkinter
from tkinter import ttk

class Interface:
    '''Класс для создания всех кнопок внутри tkinter'''
    
    def __init__(self, mainself, display):
        
        self.set_top_pannel(mainself, display)
        
        self.file_frame = None
    
    def set_top_pannel(self, mainself, display):
        '''установка верхней панели'''
        
        frame = ttk.Frame(display.root, padding=10)
        frame.pack(fill=tkinter.X)
        

        self.file_frame = ttk.Label(frame, text="Файл не выбран")
        self.file_frame.pack(side=tkinter.LEFT, padx=5)

        load_btn = ttk.Button(frame, text="Загрузить CSV", command=lambda: self.load_csv(mainself,display))
        load_btn.pack(side=tkinter.LEFT, padx=5)
    
    def load_csv(self, mainself, display):
        pass