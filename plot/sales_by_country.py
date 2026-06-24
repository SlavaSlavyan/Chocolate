from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return
    
    data = display.data_frame.dropna(subset=['Country', 'Amount'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк с страной и суммой.")
        return
    
    data = data.groupby('Country')['Amount'].sum().sort_values(ascending=False)
    
    if data.empty:
        messagebox.showwarning("Нет данных", "После группировки нет данных.")
        return

    graph, ax = plot.subplots(figsize=(10, 5))
    
    data.plot(kind='bar', ax=ax, color='lightgreen')
    
    ax.set_title('Продажи по странам')
    ax.set_xlabel('Страна')
    ax.set_ylabel('Сумма')
    
    plot.xticks(rotation=45)
    plot.tight_layout()
    
    display.draw_graph(graph)