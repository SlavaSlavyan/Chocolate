import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Создаем главное окно Tkinter
root = tk.Tk()
root.title("Маленький график в Tkinter")
root.geometry("400x300")

# 1. Создаем фигуру Matplotlib и задаем её размер в дюймах (figsize)
# 3x2 дюйма — это примерно 300x200 пикселей (при dpi=100)
fig = Figure(figsize=(3, 2), dpi=100)
ax = fig.add_subplot(111)

# Данные для графика
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]
ax.plot(x, y, marker='o')
ax.set_title("Пример", fontsize=10)

# 2. Превращаем фигуру в Tkinter-виджет с помощью FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

# 3. Размещаем холст на окне (встраиваем как обычный виджет)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=20) 

# Кнопка для закрытия
button_quit = tk.Button(root, text="Выход", command=root.quit)
button_quit.pack()

# Запуск главного цикла
root.mainloop()