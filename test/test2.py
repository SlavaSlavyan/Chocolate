import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SalesAnalyticsApp:
    """Приложение для анализа данных о продажах из CSV."""

    def __init__(self, root):
        self.root = root
        self.root.title("Аналитика продаж")
        self.root.geometry("1200x800")
        self.df = None

        # Стилизация
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', font=('Arial', 10))

        # Верхняя панель загрузки файла
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill=tk.X)

        self.file_label = ttk.Label(top_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=5)

        load_btn = ttk.Button(top_frame, text="Загрузить CSV", command=self.load_csv)
        load_btn.pack(side=tk.LEFT, padx=5)

        # Основная область с панелью выбора графика и самим графиком
        paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Левая панель с кнопками аналитики
        left_frame = ttk.LabelFrame(paned, text="Выбор анализа", padding=10)
        paned.add(left_frame, weight=0)

        analyses = [
            ("Месячная выручка", self.plot_monthly_revenue),
            ("Продажи по продуктам", self.plot_sales_by_product),
            ("Продажи по странам", self.plot_sales_by_country),
            ("Продажи по каналам", self.plot_sales_by_channel),
            ("Топ-10 продавцов", self.plot_top_salespersons),
            ("Скидка vs Сумма", self.plot_discount_vs_amount),
            ("Маркетинг vs Коробки", self.plot_marketing_vs_boxes),
            ("Распределение скидок", self.plot_discount_distribution),
        ]
        for text, command in analyses:
            btn = ttk.Button(left_frame, text=text, command=command)
            btn.pack(fill=tk.X, pady=3)

        # Правая панель для отображения графика
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)

        self.plot_frame = ttk.Frame(right_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Статусная строка
        self.status = ttk.Label(root, text="Готов", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def load_csv(self):
        """Загрузка CSV-файла и проверка обязательных колонок."""
        filepath = filedialog.askopenfilename(
            title="Выберите CSV файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return
        try:
            # Парсинг даты для дальнейшей аналитики
            self.df = pd.read_csv(filepath, parse_dates=['Order_Date'])
            required = [
                'Order_ID', 'Product', 'Country', 'Channel', 'Salesperson',
                'Order_Date', 'Discount_Pct', 'Price_per_Box', 'Marketing_Spend',
                'Boxes_Shipped', 'Amount'
            ]
            missing = [col for col in required if col not in self.df.columns]
            if missing:
                messagebox.showerror("Ошибка", f"Отсутствуют столбцы: {missing}")
                self.df = None
                return
            self.file_label.config(text=filepath.split('/')[-1])
            self.status.config(text=f"Загружено {len(self.df)} записей")
            # Очищаем предыдущий график
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
            self.df = None

    def clear_plot(self):
        """Удаление текущего графика."""
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def draw_plot(self, fig):
        """Отображение Matplotlib Figure в интерфейсе."""
        self.clear_plot()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ----------------------------------------------------------------------
    # Методы для каждого вида аналитики
    # ----------------------------------------------------------------------
    def plot_monthly_revenue(self):
        if not self._check_df():
            return
        df = self.df.copy()
        df['Month'] = df['Order_Date'].dt.to_period('M')
        monthly = df.groupby('Month')['Amount'].sum().reset_index()
        monthly['Month'] = monthly['Month'].astype(str)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly['Month'], monthly['Amount'], marker='o', color='b')
        ax.set_title('Месячная выручка')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Сумма')
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_sales_by_product(self):
        if not self._check_df():
            return
        data = self.df.groupby('Product')['Amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        data.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title('Продажи по продуктам')
        ax.set_xlabel('Продукт')
        ax.set_ylabel('Сумма')
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_sales_by_country(self):
        if not self._check_df():
            return
        data = self.df.groupby('Country')['Amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        data.plot(kind='bar', ax=ax, color='lightgreen')
        ax.set_title('Продажи по странам')
        ax.set_xlabel('Страна')
        ax.set_ylabel('Сумма')
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_sales_by_channel(self):
        if not self._check_df():
            return
        data = self.df.groupby('Channel')['Amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        data.plot(kind='bar', ax=ax, color='salmon')
        ax.set_title('Продажи по каналам')
        ax.set_xlabel('Канал')
        ax.set_ylabel('Сумма')
        plt.xticks(rotation=0)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_top_salespersons(self):
        if not self._check_df():
            return
        data = self.df.groupby('Salesperson')['Amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        data.plot(kind='barh', ax=ax, color='gold')
        ax.set_title('Топ-10 продавцов')
        ax.set_xlabel('Сумма')
        ax.set_ylabel('Продавец')
        ax.invert_yaxis()
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_discount_vs_amount(self):
        if not self._check_df():
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(self.df['Discount_Pct'], self.df['Amount'], alpha=0.5, c='blue')
        ax.set_title('Скидка vs Сумма продажи')
        ax.set_xlabel('Скидка (%)')
        ax.set_ylabel('Сумма')
        ax.grid(True)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_marketing_vs_boxes(self):
        if not self._check_df():
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(self.df['Marketing_Spend'], self.df['Boxes_Shipped'], alpha=0.5, c='green')
        ax.set_title('Маркетинговые расходы vs Отгруженные коробки')
        ax.set_xlabel('Маркетинговые расходы')
        ax.set_ylabel('Количество коробок')
        ax.grid(True)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_discount_distribution(self):
        if not self._check_df():
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(self.df['Discount_Pct'], bins=20, color='orange', edgecolor='black')
        ax.set_title('Распределение скидок')
        ax.set_xlabel('Скидка (%)')
        ax.set_ylabel('Частота')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        self.draw_plot(fig)

    def _check_df(self):
        """Проверяет, загружены ли данные, иначе показывает предупреждение."""
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите CSV файл")
            return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = SalesAnalyticsApp(root)
    root.mainloop()