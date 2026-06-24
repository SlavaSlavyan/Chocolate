from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return
    
    data = display.data_frame.dropna(subset=['Salesperson', 'Amount'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк с продавцом и суммой.")
        return
    
    data = data.groupby('Salesperson')['Amount'].sum().sort_values(ascending=False).head(10)
    
    if data.empty:
        messagebox.showwarning("Нет данных", "После группировки нет данных.")
        return

    graph, ax = plot.subplots(figsize=(10, 5))
    
    data.plot(kind='barh', ax=ax, color='gold')
    
    ax.set_title('Топ-10 продавцов')
    ax.set_xlabel('Сумма')
    ax.set_ylabel('Продавец')
    ax.invert_yaxis()
    
    plot.tight_layout()
    display.draw_graph(graph)