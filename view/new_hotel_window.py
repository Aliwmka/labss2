import tkinter as tk
from tkinter import ttk, messagebox

class NewHotelWindow(tk.Toplevel):
    """Диалоговое окно для добавления или редактирования отеля."""
    
    def __init__(self, parent, hotel_id=None, name="", city="", address="", stars=3, has_pool=False):
        super().__init__(parent)
        self.title("Новый отель" if hotel_id is None else "Редактировать отель")
        self.geometry("400x300")
        self.grab_set()  # Модальное окно

        self.result = None

        # Поле ID (только для чтения)
        tk.Label(self, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.id_var = tk.StringVar()
        self.id_var.set(str(hotel_id) if hotel_id else "")
        tk.Entry(self, textvariable=self.id_var, state="readonly", width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Поле Название
        tk.Label(self, text="Название:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name_var = tk.StringVar(value=name)
        tk.Entry(self, textvariable=self.name_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        # Поле Город
        tk.Label(self, text="Город:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.city_var = tk.StringVar(value=city)
        tk.Entry(self, textvariable=self.city_var, width=30).grid(row=2, column=1, padx=5, pady=5)

        # Поле Адрес
        tk.Label(self, text="Адрес:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.address_var = tk.StringVar(value=address)
        tk.Entry(self, textvariable=self.address_var, width=30).grid(row=3, column=1, padx=5, pady=5)

        # Поле Звезды
        tk.Label(self, text="Звезды:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.stars_var = tk.IntVar(value=stars)
        stars_frame = tk.Frame(self)
        stars_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        for i in range(1, 6):
            tk.Radiobutton(stars_frame, text=str(i), variable=self.stars_var, value=i).pack(side="left")

        # Поле Бассейн
        tk.Label(self, text="Бассейн:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.pool_var = tk.BooleanVar(value=has_pool)
        ttk.Checkbutton(self, text="Есть бассейн", variable=self.pool_var).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Отменить", command=self.destroy).pack(side="left", padx=5)

    def validate(self):
        """Проверка введённых данных."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Название отеля не может быть пустым!")
            return False

        city = self.city_var.get().strip()
        if not city:
            messagebox.showerror("Ошибка", "Город не может быть пустым!")
            return False

        address = self.address_var.get().strip()
        if not address:
            messagebox.showerror("Ошибка", "Адрес не может быть пустым!")
            return False

        return True

    def save(self):
        """Сохранение данных."""
        if not self.validate():
            return

        try:
            hotel_id = int(self.id_var.get()) if self.id_var.get() else None
        except ValueError:
            hotel_id = None

        self.result = {
            "id": hotel_id,
            "name": self.name_var.get().strip(),
            "city": self.city_var.get().strip(),
            "address": self.address_var.get().strip(),
            "stars": self.stars_var.get(),
            "has_pool": self.pool_var.get()
        }
        self.destroy()