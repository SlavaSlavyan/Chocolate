import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import queue

class SalesAnalyticsBigDataApp:
    """Приложение для анализа больших CSV с продажами (агрегация в потоке)."""

    def __init__(self, root):
        self.root = root
        self.root.title("Аналитика продаж (Big Data)")
        self.root.geometry("1200x800")

        # Словарь для агрегированных данных
        self.aggregates = {
            'monthly': pd.Series(dtype=float),
            'by_product': pd.Series(dtype=float),
            'by_country': pd.Series(dtype=float),
            'by_channel': pd.Series(dtype=float),
            'by_salesperson': pd.Series(dtype=float),
            'discount_amount_sample': pd.DataFrame(),   # выборка для scatter
            'marketing_boxes_sample': pd.DataFrame(),
            'discount_sample': pd.Series(dtype=float),  # для гистограммы
        }

        # Очередь для общения с потоком загрузки
        self.load_queue = queue.Queue()
        self.load_thread = None

        # Стиль
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', font=('Arial', 10))

        # === Верхняя панель: выбор файла и прогресс ===
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill=tk.X)

        self.file_label = ttk.Label(top_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=5)

        load_btn = ttk.Button(top_frame, text="Загрузить CSV", command=self.start_loading)
        load_btn.pack(side=tk.LEFT, padx=5)

        # Прогресс-бар и статус
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress = ttk.Progressbar(top_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.status_label = ttk.Label(top_frame, text="")
        self.status_label.pack(side=tk.LEFT, padx=5)

        # === Выбор аналитики ===
        paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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

        # Правая панель для графика
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        self.plot_frame = ttk.Frame(right_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Статусная строка
        self.status = ttk.Label(root, text="Готов", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Запуск мониторинга очереди из потока
        self.check_queue()

    # ----------------------------------------------------------------------
    # Загрузка с потоковой обработкой
    # ----------------------------------------------------------------------
    def start_loading(self):
        """Запуск загрузки в фоновом потоке."""
        filepath = filedialog.askopenfilename(
            title="Выберите CSV файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        # Блокируем кнопку, чтобы не запустить второй поток
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.state(['disabled'])
        self.progress_var.set(0)
        self.status_label.config(text="Загрузка...")
        self.file_label.config(text=filepath.split('/')[-1])

        # Очищаем предыдущий график
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Создаём и запускаем поток
        self.load_thread = threading.Thread(
            target=self.load_csv_worker,
            args=(filepath,),
            daemon=True
        )
        self.load_thread.start()

    def load_csv_worker(self, filepath):
        """Потоковая загрузка CSV и агрегация данных (выполняется в фоне)."""
        try:
            # Инициализируем накопительные серии
            monthly = pd.Series(dtype=float)
            product = pd.Series(dtype=float)
            country = pd.Series(dtype=float)
            channel = pd.Series(dtype=float)
            salesperson = pd.Series(dtype=float)

            # Для scatter-графиков сохраняем ограниченную случайную выборку
            MAX_SCATTER = 10_000
            discount_list = []
            amount_list = []
            marketing_list = []
            boxes_list = []
            discount_all = []  # для гистограммы

            # Читаем CSV чанками
            chunk_size = 50_000
            reader = pd.read_csv(
                filepath,
                parse_dates=['Order_Date'],
                chunksize=chunk_size
            )

            total_rows = 0
            for i, chunk in enumerate(reader):
                # 1. Месячная агрегация
                chunk['Month'] = chunk['Order_Date'].dt.to_period('M')
                chunk_monthly = chunk.groupby('Month')['Amount'].sum()
                monthly = monthly.add(chunk_monthly, fill_value=0)

                # 2. Продукты
                chunk_product = chunk.groupby('Product')['Amount'].sum()
                product = product.add(chunk_product, fill_value=0)

                # 3. Страны
                chunk_country = chunk.groupby('Country')['Amount'].sum()
                country = country.add(chunk_country, fill_value=0)

                # 4. Каналы
                chunk_channel = chunk.groupby('Channel')['Amount'].sum()
                channel = channel.add(chunk_channel, fill_value=0)

                # 5. Продавцы
                chunk_sales = chunk.groupby('Salesperson')['Amount'].sum()
                salesperson = salesperson.add(chunk_sales, fill_value=0)

                # 6. Выборка для scatter и гистограммы
                if len(discount_list) < MAX_SCATTER:
                    n_needed = MAX_SCATTER - len(discount_list)
                    sample = chunk.sample(n=min(n_needed, len(chunk)), random_state=42)
                    discount_list.append(sample['Discount_Pct'].values)
                    amount_list.append(sample['Amount'].values)
                    marketing_list.append(sample['Marketing_Spend'].values)
                    boxes_list.append(sample['Boxes_Shipped'].values)

                # Для гистограммы тоже берём сэмпл
                if len(discount_all) < MAX_SCATTER * 2:
                    n_needed = MAX_SCATTER * 2 - len(discount_all)
                    sample_disc = chunk['Discount_Pct'].sample(
                        n=min(n_needed, len(chunk)), random_state=42)
                    discount_all.append(sample_disc.values)

                total_rows += len(chunk)

                # Отправляем прогресс в главный поток
                progress_pct = min(100, int((total_rows / (total_rows + chunk_size)) * 100))  # приблизительно
                self.load_queue.put(('progress', progress_pct, f"Обработано {total_rows:,} строк..."))

            # Финализируем агрегаты
            self.aggregates['monthly'] = monthly.sort_index()
            self.aggregates['by_product'] = product.sort_values(ascending=False)
            self.aggregates['by_country'] = country.sort_values(ascending=False)
            self.aggregates['by_channel'] = channel.sort_values(ascending=False)
            self.aggregates['by_salesperson'] = salesperson.sort_values(ascending=False)

            # Собираем выборки в DataFrame
            if discount_list:
                self.aggregates['discount_amount_sample'] = pd.DataFrame({
                    'Discount_Pct': np.concatenate(discount_list),
                    'Amount': np.concatenate(amount_list)
                })
                self.aggregates['marketing_boxes_sample'] = pd.DataFrame({
                    'Marketing_Spend': np.concatenate(marketing_list),
                    'Boxes_Shipped': np.concatenate(boxes_list)
                })
                self.aggregates['discount_sample'] = np.concatenate(discount_all)[:MAX_SCATTER*2]
            else:
                self.aggregates['discount_amount_sample'] = pd.DataFrame()
                self.aggregates['marketing_boxes_sample'] = pd.DataFrame()
                self.aggregates['discount_sample'] = np.array([])

            self.load_queue.put(('done', total_rows, ""))

        except Exception as e:
            self.load_queue.put(('error', str(e), ""))

    def check_queue(self):
        """Периодическая проверка сообщений от потока загрузки."""
        try:
            while True:
                msg = self.load_queue.get_nowait()
                msg_type = msg[0]
                if msg_type == 'progress':
                    _, pct, text = msg
                    self.progress_var.set(pct)
                    self.status_label.config(text=text)
                elif msg_type == 'done':
                    _, total_rows, _ = msg
                    self.progress_var.set(100)
                    self.status_label.config(text=f"Загружено {total_rows:,} строк")
                    self.status.config(text="Готов к анализу")
                    self._enable_buttons()
                elif msg_type == 'error':
                    _, error_msg, _ = msg
                    messagebox.showerror("Ошибка загрузки", error_msg)
                    self.progress_var.set(0)
                    self.status_label.config(text="Ошибка")
                    self._enable_buttons()
        except queue.Empty:
            pass
        finally:
            # Проверять очередь каждые 100 мс
            self.root.after(100, self.check_queue)

    def _enable_buttons(self):
        """Разблокировать кнопки после загрузки."""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.state(['!disabled'])

    # ----------------------------------------------------------------------
    # Графики на основе агрегированных данных
    # ----------------------------------------------------------------------
    def clear_plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def draw_plot(self, fig):
        self.clear_plot()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _check_agg(self):
        if self.aggregates['monthly'].empty and self.aggregates['by_product'].empty:
            messagebox.showwarning("Нет данных", "Сначала загрузите CSV файл.")
            return False
        return True

    def plot_monthly_revenue(self):
        if not self._check_agg(): return
        s = self.aggregates['monthly']
        s.index = s.index.astype(str)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(s.index, s.values, marker='o', color='b')
        ax.set_title('Месячная выручка')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Сумма')
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_sales_by_product(self):
        if not self._check_agg(): return
        s = self.aggregates['by_product']
        fig, ax = plt.subplots(figsize=(10, 5))
        s.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title('Продажи по продуктам')
        ax.set_xlabel('Продукт')
        ax.set_ylabel('Сумма')
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_sales_by_country(self):
        if not self._check_agg(): return
        s = self.aggregates['by_country']
        fig, ax = plt.subplots(figsize=(10, 5))
        s.plot(kind='bar', ax=ax, color='lightgreen')
        ax.set_title('Продажи по странам')
        ax.set_xlabel('Страна')
        ax.set_ylabel('Сумма')
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_sales_by_channel(self):
        if not self._check_agg(): return
        s = self.aggregates['by_channel']
        fig, ax = plt.subplots(figsize=(10, 5))
        s.plot(kind='bar', ax=ax, color='salmon')
        ax.set_title('Продажи по каналам')
        ax.set_xlabel('Канал')
        ax.set_ylabel('Сумма')
        plt.xticks(rotation=0)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_top_salespersons(self):
        if not self._check_agg(): return
        s = self.aggregates['by_salesperson'].head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        s.plot(kind='barh', ax=ax, color='gold')
        ax.set_title('Топ-10 продавцов')
        ax.set_xlabel('Сумма')
        ax.set_ylabel('Продавец')
        ax.invert_yaxis()
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_discount_vs_amount(self):
        if not self._check_agg(): return
        df = self.aggregates['discount_amount_sample']
        if df.empty:
            messagebox.showinfo("Пусто", "Нет данных для scatter-графика.")
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(df['Discount_Pct'], df['Amount'], alpha=0.5, c='blue')
        ax.set_title(f'Скидка vs Сумма (выборка {len(df)} точек)')
        ax.set_xlabel('Скидка (%)')
        ax.set_ylabel('Сумма')
        ax.grid(True)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_marketing_vs_boxes(self):
        if not self._check_agg(): return
        df = self.aggregates['marketing_boxes_sample']
        if df.empty:
            messagebox.showinfo("Пусто", "Нет данных для scatter-графика.")
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(df['Marketing_Spend'], df['Boxes_Shipped'], alpha=0.5, c='green')
        ax.set_title(f'Маркетинг vs Коробки (выборка {len(df)} точек)')
        ax.set_xlabel('Маркетинговые расходы')
        ax.set_ylabel('Количество коробок')
        ax.grid(True)
        plt.tight_layout()
        self.draw_plot(fig)

    def plot_discount_distribution(self):
        if not self._check_agg(): return
        data = self.aggregates['discount_sample']
        if len(data) == 0:
            messagebox.showinfo("Пусто", "Нет данных для гистограммы.")
            return
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(data, bins=30, color='orange', edgecolor='black')
        ax.set_title(f'Распределение скидок (выборка {len(data)} точек)')
        ax.set_xlabel('Скидка (%)')
        ax.set_ylabel('Частота')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        self.draw_plot(fig)


if __name__ == "__main__":
    root = tk.Tk()
    app = SalesAnalyticsBigDataApp(root)
    root.mainloop()