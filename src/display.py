import tkinter
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        
    def clear_graph(self):
        '''удаление текущего графика'''
        
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
    def draw_graph(self, graph):
        '''отображение переданого графика'''
        
        self.clear_graph()
        
        canvas = FigureCanvasTkAgg(graph, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
    
    def check_data(self) -> bool:
        '''Проверка загрузки данных'''
        
        if self.data_frame is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите CSV файл")
            return False
        
        if self.data_frame.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для анализа")
            return False
        
        return True