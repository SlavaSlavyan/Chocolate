import tkinter
from tkinter import ttk

# все функции для графиков
from plot.discount_distribution import func as discount_distribution
from plot.discount_vs_amount import func as discount_vs_amount
from plot.marketing_vs_boxes import func as marketing_vs_boxes
from plot.monthly_revenue import func as monthly_revenue
from plot.sales_by_channel import func as sales_by_channel
from plot.sales_by_country import func as sales_by_country
from plot.sales_by_product import func as sales_by_product
from plot.top_salespersons import func as top_salespersons

class Interface:
    '''Класс для создания всех кнопок внутри tkinter'''
    
    def __init__(self, mainself, display):
        
        self.set_top_pannel(mainself, display)
        self.set_paned(mainself, display)
        self.set_status(mainself, display)
    
    def set_top_pannel(self, mainself, display):
        '''установка верхней панели'''
        
        frame = ttk.Frame(display.root, padding=10)
        frame.pack(fill=tkinter.X)

        display.file_frame = ttk.Label(frame, text="Файл не выбран")
        display.file_frame.pack(side=tkinter.LEFT, padx=5)

        load_btn = ttk.Button(frame, text="Загрузить CSV", command=lambda: mainself.Values.load(display))
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
        
        # пришлось подключать к каждой кнопке вучную :(
        
        btn = ttk.Button(frame, text="Месячная выручка", command=lambda: monthly_revenue(display))
        btn.pack(fill=tkinter.X, pady=3)
        
        btn = ttk.Button(frame, text="Продажи по продуктам", command=lambda: sales_by_product(display))
        btn.pack(fill=tkinter.X, pady=3)
        
        btn = ttk.Button(frame, text="Продажи по странам", command=lambda: sales_by_country(display))
        btn.pack(fill=tkinter.X, pady=3)
        
        btn = ttk.Button(frame, text="Продажи по каналам", command=lambda: sales_by_channel(display))
        btn.pack(fill=tkinter.X, pady=3)
        
        btn = ttk.Button(frame, text="Топ-10 продавцов", command=lambda: top_salespersons(display))
        btn.pack(fill=tkinter.X, pady=3)
        
        btn = ttk.Button(frame, text="Скидка vs Сумма", command=lambda: discount_vs_amount(display))
        btn.pack(fill=tkinter.X, pady=3)
        
        btn = ttk.Button(frame, text="Маркетинг vs Коробки", command=lambda: marketing_vs_boxes(display))
        btn.pack(fill=tkinter.X, pady=3)
        
        btn = ttk.Button(frame, text="Распределение скидок", command=lambda: discount_distribution(display))
        btn.pack(fill=tkinter.X, pady=3)
        
    def set_right_pannel(self, mainself, display, paned):
        '''Установка правой панели с графиком'''
        
        frame = ttk.Frame(paned)
        paned.add(frame, weight=1)

        display.graph_frame = ttk.Frame(frame)
        display.graph_frame.pack(fill=tkinter.BOTH, expand=True)
        
    def set_status(self, mainself, display):
        
        display.status = ttk.Label(display.root, text="Готов", relief=tkinter.SUNKEN, anchor=tkinter.W)
        display.status.pack(side=tkinter.BOTTOM, fill=tkinter.X)