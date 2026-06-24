from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return
    
    data = display.data_frame.dropna(subset=['Discount_Pct', 'Amount'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк со скидкой и суммой.")
        return

    graph, ax = plot.subplots(figsize=(10, 5))
    
    ax.scatter(data['Discount_Pct'], data['Amount'], alpha=0.5, c='blue')
    ax.set_title('Скидка vs Сумма продажи')
    ax.set_xlabel('Скидка (%)')
    ax.set_ylabel('Сумма')
    ax.grid(True)
    
    plot.tight_layout()
    
    display.draw_graph(graph)