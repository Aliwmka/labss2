import customtkinter as ctk
from tkinter import ttk, messagebox
from view.new_hotel_window import NewHotelWindow

class CustomHotelWindow(ctk.CTkToplevel):
    def __init__(self, parent, view_model):
        super().__init__(parent)
        self.title("🏨 Управление отелями")
        self.geometry("1100x650")
        self.vm = view_model
        
        self.create_interface()
        self.refresh_table()

    def create_interface(self):
        """Создание интерфейса управления отелями"""
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
            text="🏨 УПРАВЛЕНИЕ ОТЕЛЯМИ",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left")
        
        # Кнопки действий
        actions_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        actions_frame.pack(side="right")
        
        action_buttons = [
            ("➕ Создать отель", self.add_hotel, "#27ae60"),
            ("✏️ Редактировать", self.edit_hotel, "#3498db"),
            ("🗑️ Удалить", self.delete_hotel, "#e74c3c")
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
            placeholder_text="🔍 Поиск по названию отеля или городу...",
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
            text="Фильтр:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        self.stars_filter = ctk.CTkComboBox(
            search_right,
            values=["Все звезды", "5 звезд", "4 звезды", "3 звезды", "2 звезды", "1 звезда"],
            width=120,
            height=35
        )
        self.stars_filter.pack(side="left", padx=(0, 10))
        self.stars_filter.set("Все звезды")
        self.stars_filter.bind("<<ComboboxSelected>>", self.on_search)
        
        self.pool_filter = ctk.CTkComboBox(
            search_right,
            values=["Все", "С бассейном", "Без бассейна"],
            width=130,
            height=35
        )
        self.pool_filter.pack(side="left")
        self.pool_filter.set("Все")
        self.pool_filter.bind("<<ComboboxSelected>>", self.on_search)

    def create_table(self, parent):
        """Создание таблицы"""
        columns = ("ID", "Название", "Город", "Адрес", "Звезды", "Бассейн")
        self.tree_frame = ctk.CTkFrame(parent)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Стилизация Treeview
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Hotel.Treeview", 
                       background="#2a2d2e",
                       foreground="white",
                       fieldbackground="#2a2d2e",
                       rowheight=35,
                       font=('TkDefaultFont', 11))
        style.configure("Hotel.Treeview.Heading", 
                       background="#3b3b3b",
                       foreground="#FFD700",
                       relief="flat",
                       font=('TkDefaultFont', 12, 'bold'))
        style.map('Hotel.Treeview', background=[('selected', '#1f6aa5')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", 
                               style="Hotel.Treeview", height=15)
        
        # Настройка колонок
        column_config = {
            "ID": 80, "Название": 250, "Город": 150, 
            "Адрес": 200, "Звезды": 100, "Бассейн": 100
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
        stars_filter = self.stars_filter.get()
        pool_filter = self.pool_filter.get()
        
        for hotel in self.vm.hotels:
            # Поиск
            if search_term and (search_term not in hotel.name.lower() and 
                              search_term not in hotel.city.lower() and
                              search_term not in hotel.address.lower()):
                continue
            
            # Фильтр по звездам
            if stars_filter != "Все звезды":
                required_stars = int(stars_filter[0])
                if hotel.stars != required_stars:
                    continue
            
            # Фильтр по бассейну
            if pool_filter == "С бассейном" and not hotel.has_pool:
                continue
            if pool_filter == "Без бассейна" and hotel.has_pool:
                continue
            
            pool = "✅ Есть" if hotel.has_pool else "❌ Нет"
            stars_display = "⭐" * hotel.stars
            
            self.tree.insert("", "end", values=(
                hotel.id, hotel.name, hotel.city, hotel.address, 
                stars_display, pool
            ))

    def get_selected_id(self):
        """Получить ID выбранного отеля"""
        selection = self.tree.selection()
        return int(self.tree.item(selection[0])["values"][0]) if selection else None

    def add_hotel(self):
        """Добавить отель"""
        dialog = NewHotelWindow(self)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.vm.add_hotel(
                    name=dialog.result["name"],
                    city=dialog.result["city"],
                    address=dialog.result["address"],
                    stars=dialog.result["stars"],
                    has_pool=dialog.result["has_pool"]
                )
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_hotel(self):
        """Редактировать отель"""
        hotel_id = self.get_selected_id()
        if not hotel_id:
            messagebox.showwarning("Внимание", "Выберите отель для редактирования.")
            return
        
        try:
            hotel = self.vm.get_hotel_by_id(hotel_id)
            dialog = NewHotelWindow(
                self,
                hotel_id=hotel.id,
                name=hotel.name,
                city=hotel.city,
                address=hotel.address,
                stars=hotel.stars,
                has_pool=hotel.has_pool
            )
            self.wait_window(dialog)
            if dialog.result:
                self.vm.update_hotel(
                    hotel_id=hotel_id,
                    name=dialog.result["name"],
                    city=dialog.result["city"],
                    address=dialog.result["address"],
                    stars=dialog.result["stars"],
                    has_pool=dialog.result["has_pool"]
                )
                self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_hotel(self):
        """Удалить отель"""
        hotel_id = self.get_selected_id()
        if not hotel_id:
            messagebox.showwarning("Внимание", "Выберите отель для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный отель?"):
            try:
                self.vm.delete_hotel(hotel_id)
                self.refresh_table()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))