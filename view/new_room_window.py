import tkinter as tk
from tkinter import ttk, messagebox

class NewRoomWindow(tk.Toplevel):
    """Диалоговое окно для добавления или редактирования номера."""
    
    def __init__(self, parent, hotels, room_id=None, hotel_id=None, room_number="", room_type="", price_per_night=0.0, is_available=True):
        super().__init__(parent)
        self.title("Новый номер" if room_id is None else "Редактировать номер")
        self.geometry("400x350")
        self.grab_set()  # Модальное окно

        self.result = None
        self.hotels = hotels

        # Поле ID (только для чтения)
        tk.Label(self, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.id_var = tk.StringVar()
        self.id_var.set(str(room_id) if room_id else "")
        tk.Entry(self, textvariable=self.id_var, state="readonly", width=10).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Выбор отеля
        tk.Label(self, text="Отель:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.hotel_var = tk.StringVar()
        hotel_names = [f"{hotel.name} ({hotel.city})" for hotel in self.hotels]
        self.hotel_combobox = ttk.Combobox(self, textvariable=self.hotel_var, values=hotel_names, state="readonly", width=27)
        self.hotel_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Установка выбранного отеля
        if hotel_id is not None:
            hotel_ids = [hotel.id for hotel in self.hotels]
            try:
                idx = hotel_ids.index(hotel_id)
                self.hotel_combobox.current(idx)
            except ValueError:
                pass

        # Поле Номер комнаты
        tk.Label(self, text="Номер:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.room_number_var = tk.StringVar(value=room_number)
        tk.Entry(self, textvariable=self.room_number_var, width=30).grid(row=2, column=1, padx=5, pady=5)

        # Поле Тип номера
        tk.Label(self, text="Тип номера:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.type_var = tk.StringVar(value=room_type)
        type_combobox = ttk.Combobox(self, textvariable=self.type_var, 
                                   values=["Стандарт", "Бизнес", "Люкс", "Премиум", "Семейный"], 
                                   state="readonly", width=27)
        type_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Поле Цена за ночь
        tk.Label(self, text="Цена за ночь:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.price_var = tk.StringVar(value=str(price_per_night))
        tk.Entry(self, textvariable=self.price_var, width=30).grid(row=4, column=1, padx=5, pady=5)

        # Поле Статус
        tk.Label(self, text="Статус:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.status_var = tk.BooleanVar(value=is_available)
        ttk.Checkbutton(self, text="Доступен для бронирования", variable=self.status_var).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Отменить", command=self.destroy).pack(side="left", padx=5)

    def validate(self):
        """Проверка введённых данных."""
        if not self.hotel_var.get():
            messagebox.showerror("Ошибка", "Выберите отель из списка!")
            return False

        room_number = self.room_number_var.get().strip()
        if not room_number:
            messagebox.showerror("Ошибка", "Номер комнаты не может быть пустым!")
            return False

        room_type = self.type_var.get().strip()
        if not room_type:
            messagebox.showerror("Ошибка", "Тип номера не может быть пустым!")
            return False

        try:
            price = float(self.price_var.get())
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть положительным числом!")
            return False

        return True

    def save(self):
        """Сохранение данных."""
        if not self.validate():
            return

        # Получаем ID выбранного отеля
        selected_hotel_name = self.hotel_var.get()
        hotel_ids = [hotel.id for hotel in self.hotels]
        hotel_names = [f"{hotel.name} ({hotel.city})" for hotel in self.hotels]
        hotel_id = hotel_ids[hotel_names.index(selected_hotel_name)]

        try:
            room_id = int(self.id_var.get()) if self.id_var.get() else None
        except ValueError:
            room_id = None

        self.result = {
            "id": room_id,
            "hotel_id": hotel_id,
            "room_number": self.room_number_var.get().strip(),
            "room_type": self.type_var.get().strip(),
            "price_per_night": float(self.price_var.get()),
            "is_available": self.status_var.get()
        }
        self.destroy()