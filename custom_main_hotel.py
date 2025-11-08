import customtkinter as ctk
from view.custom_hotel_window import CustomHotelWindow
from view.custom_room_window import CustomRoomWindow
from viewmodel.hotel_viewmodel import HotelViewModel
from viewmodel.room_viewmodel import RoomViewModel
from service.json_service import JSONService

class CustomMainWindow(ctk.CTk):
    def __init__(self, hotel_vm, room_vm):
        super().__init__()
        
        # Настройка темы и цветов в золотых тонах
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("🏨 Luxury Hotel Management")
        self.geometry("1300x750")
        self.hotel_vm = hotel_vm
        self.room_vm = room_vm
        
        self.create_sidebar()
        self.create_main_content()
        self.refresh_data()

    def create_sidebar(self):
        """Создание боковой панели в стиле люкс"""
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Логотип
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(30, 20), padx=20, fill="x")
        
        ctk.CTkLabel(
            logo_frame, 
            text="🏨 LUXURY", 
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFD700"
        ).pack()
        
        ctk.CTkLabel(
            logo_frame, 
            text="HOTEL SYSTEM", 
            font=ctk.CTkFont(size=14),
            text_color="#b0b0b0"
        ).pack()
        
        # Навигация
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(pady=30, padx=15, fill="x")
        
        nav_items = [
            ("🏨 Отели", self.show_hotels_section, "#FFD700"),
            ("🛏️ Номера", self.show_rooms_section, "#FF6B35"),
            ("📊 Статистика", self.show_stats_section, "#00CED1")
        ]
        
        for text, command, color in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=self.adjust_color(color, -30),
                height=45,
                font=ctk.CTkFont(size=15, weight="bold"),
                corner_radius=8
            )
            btn.pack(pady=8, fill="x")
        
        # Быстрые действия
        quick_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        quick_frame.pack(pady=20, padx=15, fill="x")
        
        ctk.CTkLabel(
            quick_frame, 
            text="БЫСТРЫЕ ДЕЙСТВИЯ", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#FFD700"
        ).pack(anchor="w", pady=(0, 10))
        
        quick_actions = [
            ("➕ Новый отель", self.open_hotels_management),
            ("🛏️ Добавить номер", self.open_rooms_management)
        ]
        
        for text, command in quick_actions:
            btn = ctk.CTkButton(
                quick_frame,
                text=text,
                command=command,
                fg_color="transparent",
                border_color="#FFD700",
                border_width=2,
                hover_color="#2a2a2a",
                height=35,
                font=ctk.CTkFont(size=12)
            )
            btn.pack(pady=4, fill="x")
        
        # Статистика
        self.create_sidebar_stats()
        
        # Переключатель темы
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.pack(side="bottom", pady=20, padx=15, fill="x")
        
        ctk.CTkLabel(theme_frame, text="Оформление:", text_color="#b0b0b0").pack(anchor="w")
        self.theme_switch = ctk.CTkSwitch(
            theme_frame, 
            text="Тёмная тема", 
            command=self.toggle_theme,
            progress_color="#FFD700",
            onvalue="dark", 
            offvalue="light"
        )
        self.theme_switch.pack(pady=5, anchor="w")
        self.theme_switch.select()

    def create_sidebar_stats(self):
        """Создание блока статистики в сайдбаре"""
        stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        stats_frame.pack(pady=20, padx=15, fill="x")
        
        ctk.CTkLabel(
            stats_frame, 
            text="СТАТИСТИКА СИСТЕМЫ", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#FFD700"
        ).pack(anchor="w", pady=(0, 15))
        
        self.stats_cards = {}
        stats_data = [
            ("🏨 Отелей", "total_hotels", "#FFD700"),
            ("🛏️ Номеров", "total_rooms", "#FF6B35"),
            ("✅ Доступно", "available_rooms", "#00CED1"),
            ("⭐ 5-звездочных", "five_star_hotels", "#9B59B6")
        ]
        
        for text, key, color in stats_data:
            card = ctk.CTkFrame(stats_frame, fg_color="#2a2a2a", corner_radius=8)
            card.pack(fill="x", pady=6)
            
            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(padx=12, pady=8, fill="x")
            
            ctk.CTkLabel(
                content_frame, 
                text=text, 
                font=ctk.CTkFont(size=11),
                text_color="#b0b0b0"
            ).pack(side="left")
            
            self.stats_cards[key] = ctk.CTkLabel(
                content_frame, 
                text="0", 
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=color
            )
            self.stats_cards[key].pack(side="right")

    def create_main_content(self):
        """Создание основного контента"""
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color="#1e1e1e")
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # Верхняя панель
        self.create_top_panel()
        
        # Контент
        self.create_content_area()

    def create_top_panel(self):
        """Создание верхней панели"""
        top_panel = ctk.CTkFrame(self.main_content, height=80, fg_color="#2a2a2a", corner_radius=0)
        top_panel.pack(fill="x", padx=0, pady=0)
        top_panel.pack_propagate(False)
        
        # Заголовок раздела
        self.section_title = ctk.CTkLabel(
            top_panel,
            text="🏨 ОБЗОР СИСТЕМЫ",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFD700"
        )
        self.section_title.pack(side="left", padx=30, pady=25)
        
        # Поиск и фильтры
        search_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        search_frame.pack(side="right", padx=30, pady=20)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Поиск отелей или номеров...",
            width=250,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

    def create_content_area(self):
        """Создание области контента"""
        # Приветственный баннер
        banner_frame = ctk.CTkFrame(self.main_content, fg_color="#2a2a2a", corner_radius=12)
        banner_frame.pack(fill="x", padx=20, pady=20)
        
        banner_content = ctk.CTkFrame(banner_frame, fg_color="transparent")
        banner_content.pack(padx=25, pady=20, fill="x")
        
        ctk.CTkLabel(
            banner_content,
            text="Добро пожаловать в Luxury Hotel System",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFD700"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            banner_content,
            text="Управляйте отелями и номерами с комфортом и стилем",
            font=ctk.CTkFont(size=14),
            text_color="#b0b0b0"
        ).pack(anchor="w", pady=(5, 0))
        
        # Основная таблица
        self.create_main_table()

    def create_main_table(self):
        """Создание основной таблицы"""
        content_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Заголовок таблицы
        table_header = ctk.CTkFrame(content_frame, fg_color="transparent")
        table_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            table_header, 
            text="🏨 ВСЕ ОТЕЛИ", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        # Фильтры
        filter_frame = ctk.CTkFrame(table_header, fg_color="transparent")
        filter_frame.pack(side="right")
        
        self.stars_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Все звезды", "5 звезд", "4 звезды", "3 звезды"],
            width=120,
            height=32
        )
        self.stars_filter.pack(side="left", padx=(0, 10))
        self.stars_filter.set("Все звезды")
        self.stars_filter.bind("<<ComboboxSelected>>", self.on_filter)
        
        # Таблица
        self.create_hotels_table(content_frame)

    def create_hotels_table(self, parent):
        """Создание таблицы отелей"""
        columns = ("ID", "Отель", "Город", "Звезды", "Бассейн", "Номеров")
        self.tree_frame = ctk.CTkFrame(parent)
        self.tree_frame.pack(fill="both", expand=True)
        
        # Стилизация Treeview
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Luxury.Treeview", 
                       background="#2a2d2e",
                       foreground="white",
                       fieldbackground="#2a2d2e",
                       rowheight=32,
                       font=('TkDefaultFont', 11))
        style.configure("Luxury.Treeview.Heading", 
                       background="#3b3b3b",
                       foreground="#FFD700",
                       relief="flat",
                       font=('TkDefaultFont', 12, 'bold'))
        style.map('Luxury.Treeview', background=[('selected', '#1f6aa5')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", 
                               style="Luxury.Treeview", height=18)
        
        # Настройка колонок
        column_config = {
            "ID": 70, "Отель": 250, "Город": 150, 
            "Звезды": 100, "Бассейн": 100, "Номеров": 100
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

    def toggle_theme(self):
        """Переключение темы"""
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def show_hotels_section(self):
        """Показать раздел отелей"""
        self.section_title.configure(text="🏨 УПРАВЛЕНИЕ ОТЕЛЯМИ")
        self.refresh_hotels_data()

    def show_rooms_section(self):
        """Показать раздел номеров"""
        self.section_title.configure(text="🛏️ УПРАВЛЕНИЕ НОМЕРАМИ")
        self.refresh_rooms_data()

    def show_stats_section(self):
        """Показать раздел статистики"""
        self.section_title.configure(text="📊 СТАТИСТИКА СИСТЕМЫ")
        self.refresh_stats_display()

    def open_hotels_management(self):
        """Открыть управление отелями"""
        window = CustomHotelWindow(self, self.hotel_vm)
        self.wait_window(window)
        self.refresh_data()

    def open_rooms_management(self):
        """Открыть управление номерами"""
        window = CustomRoomWindow(self, self.room_vm, self.hotel_vm)
        self.wait_window(window)
        self.refresh_data()

    def on_search(self, event):
        """Обработка поиска"""
        self.refresh_data()

    def on_filter(self, event):
        """Обработка фильтра"""
        self.refresh_data()

    def refresh_data(self):
        """Обновление всех данных"""
        self.refresh_stats()
        self.refresh_hotels_data()

    def refresh_stats(self):
        """Обновление статистики"""
        total_hotels = len(self.hotel_vm.hotels)
        total_rooms = len(self.room_vm.rooms)
        available_rooms = sum(1 for room in self.room_vm.rooms if room.is_available)
        five_star_hotels = sum(1 for hotel in self.hotel_vm.hotels if hotel.stars == 5)
        
        self.stats_cards["total_hotels"].configure(text=str(total_hotels))
        self.stats_cards["total_rooms"].configure(text=str(total_rooms))
        self.stats_cards["available_rooms"].configure(text=str(available_rooms))
        self.stats_cards["five_star_hotels"].configure(text=str(five_star_hotels))

    def refresh_hotels_data(self):
        """Обновление данных отелей"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_entry.get().lower()
        stars_filter = self.stars_filter.get()
        
        for hotel in self.hotel_vm.hotels:
            if search_term and search_term not in hotel.name.lower() and search_term not in hotel.city.lower():
                continue
                
            if stars_filter != "Все звезды":
                required_stars = int(stars_filter[0])
                if hotel.stars != required_stars:
                    continue
            
            # Подсчет номеров в отеле
            room_count = sum(1 for room in self.room_vm.rooms if room.hotel_id == hotel.id)
            
            pool = "✅ Есть" if hotel.has_pool else "❌ Нет"
            stars_display = "⭐" * hotel.stars
            
            self.tree.insert("", "end", values=(
                hotel.id, hotel.name, hotel.city, stars_display, pool, room_count
            ))

    def refresh_rooms_data(self):
        """Обновление данных номеров"""
        # В реальном приложении можно переключать таблицу
        pass

    def refresh_stats_display(self):
        """Обновление отображения статистики"""
        # В реальном приложении можно показать графики и диаграммы
        pass

def main():
    json_service = JSONService()
    hotel_vm = HotelViewModel(json_service)
    room_vm = RoomViewModel(hotel_vm, json_service)

    app = CustomMainWindow(hotel_vm, room_vm)
    app.mainloop()

if __name__ == "__main__":
    main()