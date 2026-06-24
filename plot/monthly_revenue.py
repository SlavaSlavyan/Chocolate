from tkinter import messagebox
import matplotlib.pyplot as plot

def func(display):
    
    if not display.check_data():
        return

    data = display.data_frame.dropna(subset=['Order_Date', 'Amount'])
    
    if data.empty:
        messagebox.showwarning("Нет данных", "Нет строк с корректной датой и суммой.")
        return

    data['Month'] = data['Order_Date'].dt.to_period('M').astype(str)
    monthly = data.groupby('Month')['Amount'].sum().reset_index()

    graph, ax = plot.subplots(figsize=(10, 5))
    
    ax.plot(monthly['Month'], monthly['Amount'], marker='o', color='b')
    ax.set_title('Месячная выручка (только корректные строки)')
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Сумма')
    ax.grid(True)
    
    plot.xticks(rotation=45)
    plot.tight_layout()
    
    display.draw_graph(graph)