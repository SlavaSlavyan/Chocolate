from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return
    
    data = display.data_frame.dropna(subset=['Channel', 'Amount'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк с каналом и суммой.")
        return
    
    data = data.groupby('Channel')['Amount'].sum().sort_values(ascending=False)
    
    if data.empty:
        messagebox.showwarning("Нет данных", "После группировки нет данных.")
        return

    graph, ax = plot.subplots(figsize=(10, 5))
    
    data.plot(kind='bar', ax=ax, color='salmon')
    
    ax.set_title('Продажи по каналам')
    ax.set_xlabel('Канал')
    ax.set_ylabel('Сумма')
    
    plot.xticks(rotation=0)
    plot.tight_layout()
    
    display.draw_graph(graph)
    