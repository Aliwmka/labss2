import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self, hotel_vm, room_vm):
        super().__init__()
        self.title("Система управления отелями")
        self.geometry("1000x600")
        self.hotel_vm = hotel_vm
        self.room_vm = room_vm

        self.create_menu()
        self.create_main_content()
        self.refresh_data()

    def create_menu(self):
        """Создание простого меню"""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # Меню "Управление"
        manage_menu = tk.Menu(menu_bar, tearoff=0)
        manage_menu.add_command(label="Управление отелями", 
                               command=lambda: self.open_hotels(self.hotel_vm))
        manage_menu.add_command(label="Управление номерами", 
                               command=lambda: self.open_rooms(self.room_vm, self.hotel_vm))
        menu_bar.add_cascade(label="Управление", menu=manage_menu)

    def create_main_content(self):
        """Создание основного содержимого"""
        # Заголовок
        title_label = tk.Label(self, text="🏨 СИСТЕМА УПРАВЛЕНИЯ ОТЕЛЯМИ", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Статистика
        self.stats_label = tk.Label(self, text="", font=("Arial", 10))
        self.stats_label.pack(pady=5)

        # Таблица всех номеров
        self.create_rooms_table()

    def create_rooms_table(self):
        """Создание таблицы со всеми номерами"""
        # Таблица
        columns = ("ID", "Отель", "Город", "Номер", "Тип", "Цена за ночь", "Статус")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        # Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Отель", text="Отель")
        self.tree.heading("Город", text="Город")
        self.tree.heading("Номер", text="Номер")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Цена за ночь", text="Цена за ночь")
        self.tree.heading("Статус", text="Статус")

        self.tree.column("ID", width=50)
        self.tree.column("Отель", width=150)
        self.tree.column("Город", width=120)
        self.tree.column("Номер", width=80)
        self.tree.column("Тип", width=100)
        self.tree.column("Цена за ночь", width=120)
        self.tree.column("Статус", width=100)

        # Скроллбар
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def refresh_data(self):
        """Обновление данных в таблице"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Обновление статистики
        total_hotels = len(self.hotel_vm.hotels)
        total_rooms = len(self.room_vm.rooms)
        available_rooms = sum(1 for room in self.room_vm.rooms if room.is_available)
        
        self.stats_label.config(
            text=f"Отелей: {total_hotels} | Номеров: {total_rooms} | Доступно номеров: {available_rooms}"
        )

        # Создаём словарь ID → отель
        hotel_map = {hotel.id: hotel for hotel in self.hotel_vm.hotels}
        
        # Заполнение таблицы номерами
        for room in self.room_vm.rooms:
            hotel = hotel_map.get(room.hotel_id)
            hotel_name = hotel.name if hotel else "Неизвестно"
            city = hotel.city if hotel else "Неизвестно"
            status = "Доступен" if room.is_available else "Занят"
            
            self.tree.insert("", "end", values=(
                room.id, 
                hotel_name,
                city,
                room.room_number, 
                room.room_type, 
                f"{room.price_per_night:.2f} руб.", 
                status
            ))

    def open_hotels(self, vm):
        """Открытие окна управления отелями"""
        from view.hotel_window import HotelWindow
        window = HotelWindow(self, vm)
        self.wait_window(window)
        self.refresh_data()

    def open_rooms(self, room_vm, hotel_vm):
        """Открытие окна управления номерами"""
        from view.room_window import RoomWindow
        window = RoomWindow(self, room_vm, hotel_vm)
        self.wait_window(window)
        self.refresh_data()