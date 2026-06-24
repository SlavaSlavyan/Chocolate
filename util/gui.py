import tkinter
from tkinter import ttk

class Interface:
    '''Класс для создания всех кнопок внутри tkinter'''
    
    def __init__(self, mainself, display):
        
        self.set_top_pannel(mainself, display)
        self.set_paned(mainself, display)
        
        self.file_frame = None
        self.graph_frame = None
    
    def set_top_pannel(self, mainself, display):
        '''установка верхней панели'''
        
        frame = ttk.Frame(display.root, padding=10)
        frame.pack(fill=tkinter.X)
        

        self.file_frame = ttk.Label(frame, text="Файл не выбран")
        self.file_frame.pack(side=tkinter.LEFT, padx=5)

        load_btn = ttk.Button(frame, text="Загрузить CSV", command=lambda: self.load_csv(mainself,display))
        load_btn.pack(side=tkinter.LEFT, padx=5)
    
    def set_paned(self, mainself, display):
        '''установка основной рабочей зоны'''
        
        paned = ttk.PanedWindow(display.root, orient=tkinter.HORIZONTAL)
        paned.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.set_left_pannel(mainself,display,paned)
        self.set_right_pannel(mainself,display,paned)
        
    def set_left_pannel(self, mainself, display, paned):
        '''Установка левой панели с кнопками'''
        
        frame = ttk.LabelFrame(paned, text="Выбор анализа", padding=10)
        paned.add(frame, weight=0)
        
        analyses = [
            ("Месячная выручка",     self.plot_monthly_revenue),
            ("Продажи по продуктам", self.plot_sales_by_product),
            ("Продажи по странам",   self.plot_sales_by_country),
            ("Продажи по каналам",   self.plot_sales_by_channel),
            ("Топ-10 продавцов",     self.plot_top_salespersons),
            ("Скидка vs Сумма",      self.plot_discount_vs_amount),
            ("Маркетинг vs Коробки", self.plot_marketing_vs_boxes),
            ("Распределение скидок", self.plot_discount_distribution)
        ]
        
        for text, command in analyses:
            btn = ttk.Button(frame, text=text, command=lambda: command(mainself,display))
            btn.pack(fill=tkinter.X, pady=3)
        
    def set_right_pannel(self, mainself, display, paned):
        '''Установка правой панели с графиком'''
        
        frame = ttk.Frame(paned)
        paned.add(frame, weight=1)

        self.plot_frame = ttk.Frame(frame)
        self.plot_frame.pack(fill=tkinter.BOTH, expand=True)
        
    def load_plot_graph(self, mainself, display, funcNum:int):
        
        print(funcNum)
        
    def load_csv(self, mainself, display):
        '''обёртка для загрузки файлов формата .csv'''
        pass
    
    # все эти переменные лишь обёртка для каждой из кнопок
    # сделано это было потому что иначе не получилось :(
    
    def plot_monthly_revenue(self, mainself, display):
        pass
    def plot_sales_by_product(self, mainself, display):
        pass
    def plot_sales_by_country(self, mainself, display):
        pass
    def plot_sales_by_channel(self, mainself, display):
        pass
    def plot_top_salespersons(self, mainself, display):
        pass
    def plot_discount_vs_amount(self, mainself, display):
        pass
    def plot_marketing_vs_boxes(self, mainself, display):
        pass
    def plot_discount_distribution(sel, mainself, display):
        pass