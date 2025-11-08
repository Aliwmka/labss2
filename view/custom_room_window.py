import customtkinter as ctk
from tkinter import ttk, messagebox
from view.new_room_window import NewRoomWindow

class CustomRoomWindow(ctk.CTkToplevel):
    def __init__(self, parent, room_vm, hotel_vm):
        super().__init__(parent)
        self.title("🛏️ Управление номерами")
        self.geometry("1200x700")
        self.room_vm = room_vm
        self.hotel_vm = hotel_vm
        
        self.create_interface()
        self.refresh_table()

    def create_interface(self):
        """Создание интерфейса управления номерами"""
        # Основной контейнер
        main_container = ctk.CTkFrame(self, fg_color="#1e1e1e")
        main_container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Заголовок
        header_frame = ctk.CTkFrame(main_container, fg_color="#2a2a2a", corner_radius=12)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(padx=25, pady=20, fill="x")
        
        ctk.CTkLabel(
            header_content,
            text="🛏️ УПРАВЛЕНИЕ НОМЕРАМИ",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF6B35"
        ).pack(side="left")
        
        # Кнопки действий
        actions_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        actions_frame.pack(side="right")
        
        action_buttons = [
            ("➕ Добавить номер", self.add_room, "#27ae60"),
            ("✏️ Редактировать", self.edit_room, "#3498db"),
            ("🗑️ Удалить", self.delete_room, "#e74c3c"),
            ("📊 Статистика", self.show_stats, "#9b59b6")
        ]
        
        for text, command, color in action_buttons:
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=self.adjust_color(color, -20),
                width=140,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            btn.pack(side="left", padx=5)
        
        # Панель поиска и фильтров
        self.create_search_panel(main_container)
        
        # Таблица
        self.create_table(main_container)

    def create_search_panel(self, parent):
        """Создание панели поиска"""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Поиск
        search_left = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_left.pack(side="left", fill="x", expand=True)
        
        self.search_entry = ctk.CTkEntry(
            search_left,
            placeholder_text="🔍 Поиск по номеру, типу или отелю...",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Фильтры
        search_right = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_right.pack(side="right", padx=(20, 0))
        
        ctk.CTkLabel(
            search_right, 
            text="Фильтры:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        # Фильтр по отелю
        hotel_names = ["Все отели"] + [f"{hotel.name} ({hotel.city})" for hotel in self.hotel_vm.hotels]
        self.hotel_filter = ctk.CTkComboBox(
            search_right,
            values=hotel_names,
            width=180,
            height=35
        )
        self.hotel_filter.pack(side="left", padx=(0, 10))
        self.hotel_filter.set("Все отели")
        self.hotel_filter.bind("<<ComboboxSelected>>", self.on_search)
        
        # Фильтр по статусу
        self.status_filter = ctk.CTkComboBox(
            search_right,
            values=["Все", "Доступны", "Заняты"],
            width=120,
            height=35
        )
        self.status_filter.pack(side="left", padx=(0, 10))
        self.status_filter.set("Все")
        self.status_filter.bind("<<ComboboxSelected>>", self.on_search)
        
        # Фильтр по типу номера
        self.type_filter = ctk.CTkComboBox(
            search_right,
            values=["Все типы", "Стандарт", "Бизнес", "Люкс", "Премиум", "Семейный"],
            width=130,
            height=35
        )
        self.type_filter.pack(side="left")
        self.type_filter.set("Все типы")
        self.type_filter.bind("<<ComboboxSelected>>", self.on_search)

    def create_table(self, parent):
        """Создание таблицы"""
        columns = ("ID", "Отель", "Номер", "Тип", "Цена за ночь", "Статус")
        self.tree_frame = ctk.CTkFrame(parent)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Стилизация Treeview
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Room.Treeview", 
                       background="#2a2d2e",
                       foreground="white",
                       fieldbackground="#2a2d2e",
                       rowheight=35,
                       font=('TkDefaultFont', 11))
        style.configure("Room.Treeview.Heading", 
                       background="#3b3b3b",
                       foreground="#FF6B35",
                       relief="flat",
                       font=('TkDefaultFont', 12, 'bold'))
        style.map('Room.Treeview', background=[('selected', '#1f6aa5')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", 
                               style="Room.Treeview", height=16)
        
        # Настройка колонок
        column_config = {
            "ID": 80, "Отель": 250, "Номер": 100, 
            "Тип": 120, "Цена за ночь": 150, "Статус": 120
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_config[col])
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def adjust_color(self, color, amount):
        """Регулировка яркости цвета"""
        import colorsys
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        l = max(0, min(1, l + amount/255))
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

    def on_search(self, event=None):
        """Обработка поиска и фильтрации"""
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_entry.get().lower()
        hotel_filter = self.hotel_filter.get()
        status_filter = self.status_filter.get()
        type_filter = self.type_filter.get()
        
        # Создаем словарь для быстрого доступа к отелям
        hotel_map = {hotel.id: f"{hotel.name} ({hotel.city})" for hotel in self.hotel_vm.hotels}
        
        for room in self.room_vm.rooms:
            hotel_name = hotel_map.get(room.hotel_id, "Неизвестно")
            
            # Поиск
            if search_term and (search_term not in room.room_number.lower() and 
                              search_term not in room.room_type.lower() and
                              search_term not in hotel_name.lower()):
                continue
            
            # Фильтр по отелю
            if hotel_filter != "Все отели" and hotel_name != hotel_filter:
                continue
            
            # Фильтр по статусу
            if status_filter == "Доступны" and not room.is_available:
                continue
            if status_filter == "Заняты" and room.is_available:
                continue
            
            # Фильтр по типу
            if type_filter != "Все типы" and room.room_type != type_filter:
                continue
            
            status = "✅ Доступен" if room.is_available else "❌ Занят"
            price = f"{room.price_per_night:,.2f} руб.".replace(",", " ")
            
            self.tree.insert("", "end", values=(
                room.id, hotel_name, room.room_number, room.room_type, price, status
            ))

    def get_selected_id(self):
        """Получить ID выбранного номера"""
        selection = self.tree.selection()
        return int(self.tree.item(selection[0])["values"][0]) if selection else None

    def add_room(self):
        """Добавить номер"""
        dialog = NewRoomWindow(self, self.hotel_vm.hotels)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.room_vm.add_room(
                    hotel_id=dialog.result["hotel_id"],
                    room_number=dialog.result["room_number"],
                    room_type=dialog.result["room_type"],
                    price_per_night=dialog.result["price_per_night"],
                    is_available=dialog.result["is_available"]
                )
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_room(self):
        """Редактировать номер"""
        room_id = self.get_selected_id()
        if not room_id:
            messagebox.showwarning("Внимание", "Выберите номер для редактирования.")
            return
        
        try:
            room = self.room_vm.get_room_by_id(room_id)
            dialog = NewRoomWindow(
                self,
                self.hotel_vm.hotels,
                room_id=room.id,
                hotel_id=room.hotel_id,
                room_number=room.room_number,
                room_type=room.room_type,
                price_per_night=room.price_per_night,
                is_available=room.is_available
            )
            self.wait_window(dialog)
            if dialog.result:
                self.room_vm.update_room(
                    room_id=room_id,
                    hotel_id=dialog.result["hotel_id"],
                    room_number=dialog.result["room_number"],
                    room_type=dialog.result["room_type"],
                    price_per_night=dialog.result["price_per_night"],
                    is_available=dialog.result["is_available"]
                )
                self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_room(self):
        """Удалить номер"""
        room_id = self.get_selected_id()
        if not room_id:
            messagebox.showwarning("Внимание", "Выберите номер для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный номер?"):
            try:
                self.room_vm.delete_room(room_id)
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def show_stats(self):
        """Показать статистику по номерам"""
        total_rooms = len(self.room_vm.rooms)
        available_rooms = sum(1 for room in self.room_vm.rooms if room.is_available)
        occupied_rooms = total_rooms - available_rooms
        
        # Статистика по типам номеров
        type_stats = {}
        for room in self.room_vm.rooms:
            if room.room_type not in type_stats:
                type_stats[room.room_type] = 0
            type_stats[room.room_type] += 1
        
        # Создаем окно статистики
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("📊 Статистика номеров")
        stats_window.geometry("500x400")
        stats_window.transient(self)
        stats_window.grab_set()
        
        main_frame = ctk.CTkFrame(stats_window, fg_color="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📊 СТАТИСТИКА НОМЕРОВ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FF6B35"
        ).pack(pady=(0, 20))
        
        # Основная статистика
        stats_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a", corner_radius=8)
        stats_frame.pack(fill="x", pady=10, padx=10)
        
        stats_data = [
            ("Всего номеров:", str(total_rooms), "#3498db"),
            ("Доступно:", str(available_rooms), "#27ae60"),
            ("Занято:", str(occupied_rooms), "#e74c3c")
        ]
        
        for text, value, color in stats_data:
            stat_row = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_row.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(
                stat_row,
                text=text,
                font=ctk.CTkFont(size=14),
                text_color="#b0b0b0"
            ).pack(side="left")
            
            ctk.CTkLabel(
                stat_row,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            ).pack(side="right")
        
        # Статистика по типам
        types_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a", corner_radius=8)
        types_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            types_frame,
            text="Распределение по типам:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFD700"
        ).pack(pady=10)
        
        for room_type, count in type_stats.items():
            type_row = ctk.CTkFrame(types_frame, fg_color="transparent")
            type_row.pack(fill="x", padx=15, pady=4)
            
            ctk.CTkLabel(
                type_row,
                text=room_type,
                font=ctk.CTkFont(size=12),
                text_color="#b0b0b0"
            ).pack(side="left")
            
            ctk.CTkLabel(
                type_row,
                text=str(count),
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#FF6B35"
            ).pack(side="right")