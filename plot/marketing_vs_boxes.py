from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return
    
    data = display.data_frame.dropna(subset=['Marketing_Spend', 'Boxes_Shipped'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк с расходами и коробками.")
        return

    graph, ax = plot.subplots(figsize=(10, 5))
    
    ax.scatter(data['Marketing_Spend'], data['Boxes_Shipped'], alpha=0.5, c='green')
    ax.set_title('Маркетинговые расходы vs Отгруженные коробки')
    ax.set_xlabel('Маркетинговые расходы')
    ax.set_ylabel('Количество коробок')
    ax.grid(True)
    
    plot.tight_layout()
    
    display.draw_graph(graph)