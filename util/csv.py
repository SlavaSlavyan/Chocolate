import tkinter
import pandas
from tkinter import filedialog, messagebox

class CSValues:
    
    def __init__(self):
        pass
    
    def load(self,display):
        """Загрузка файлов .csv"""
        
        filepath = filedialog.askopenfilename(
            title="Выберите CSV файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:

            buffer = pandas.read_csv(filepath, dtype=str)  # всё как строки для безопасной очистки

            required = [
                'Order_ID', 'Product', 'Country', 'Channel', 'Salesperson',
                'Order_Date', 'Discount_Pct', 'Price_per_Box', 'Marketing_Spend',
                'Boxes_Shipped', 'Amount'
            ]
            
            missing = [col for col in required if col not in buffer.columns]
            if missing:
                messagebox.showerror("Ошибка", f"Отсутствуют столбцы: {missing}")
                return

            buffer['Order_Date'] = pandas.to_datetime(buffer['Order_Date'], errors='coerce')

            def clean_numeric(series):
                return series.astype(str).str.replace(r'[^\d\.\-]', '', regex=True)

            numeric_cols = ['Discount_Pct', 'Price_per_Box', 'Marketing_Spend',
                            'Boxes_Shipped', 'Amount']
            
            for col in numeric_cols:
                buffer[col] = pandas.to_numeric(clean_numeric(buffer[col]), errors='coerce')

            # сохраняем данные
            display.data_frame = buffer
            total_rows = len(buffer)
           
            problem_mask = buffer[['Order_Date', 'Amount', 'Product', 'Country', 'Channel']].isna().any(axis=1)
            bad_rows = problem_mask.sum()
            good_rows = total_rows - bad_rows

            display.file_frame.config(text=filepath.split('/')[-1])
            display.status.config(
                text=f"Загружено {total_rows} строк. "
                     f"Полностью корректных: {good_rows}, проблемных (будут пропущены в графиках): {bad_rows}"
            )

            # Очищаем предыдущий график
            for widget in display.graph_frame.winfo_children():
                widget.destroy()

            if good_rows == 0:
                messagebox.showwarning("Предупреждение", "Нет ни одной строки с полными данными для анализа.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
            display.data_frame = None