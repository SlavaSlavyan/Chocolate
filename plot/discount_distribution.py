from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return
    
    data = display.data_frame.dropna(subset=['Discount_Pct'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк со скидкой.")
        return

    graph, ax = plot.subplots(figsize=(10, 5))
    
    ax.hist(data['Discount_Pct'], bins=20, color='orange', edgecolor='black')
    ax.set_title('Распределение скидок')
    ax.set_xlabel('Скидка (%)')
    ax.set_ylabel('Частота')
    ax.grid(True, alpha=0.3)
    
    plot.tight_layout()
    
    display.draw_graph(graph)