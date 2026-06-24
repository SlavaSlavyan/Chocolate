from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return
    
    data = display.data_frame.dropna(subset=['Product', 'Amount'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк с продуктом и суммой.")
        return
    
    data = data.groupby('Product')['Amount'].sum().sort_values(ascending=False)
    
    if data.empty:
        messagebox.showwarning("Нет данных", "После группировки нет данных.")
        return

    graph, ax = plot.subplots(figsize=(10, 5))
    
    data.plot(kind='bar', ax=ax, color='skyblue')
    
    ax.set_title('Продажи по продуктам')
    ax.set_xlabel('Продукт')
    ax.set_ylabel('Сумма')
    
    plot.xticks(rotation=45)
    plot.tight_layout()
    
    display.draw_graph(graph)