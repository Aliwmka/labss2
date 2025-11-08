import customtkinter as ctk
from view.custom_hotel_window import CustomHotelWindow
from view.custom_room_window import CustomRoomWindow
from viewmodel.hotel_viewmodel import HotelViewModel
from viewmodel.room_viewmodel import RoomViewModel
from service.json_service import JSONService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

class CustomMainWindow(ctk.CTk):
    def __init__(self, hotel_vm, room_vm):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("🏨 Luxury Hotel Management")
        self.geometry("1300x750")
        self.hotel_vm = hotel_vm
        self.room_vm = room_vm
        self.current_section = "hotels"
        
        self.create_sidebar()
        self.create_main_content()
        self.refresh_data()

    def create_sidebar(self):
        """Создание боковой панели"""
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
            ("🏨 Отели", "hotels", "#FFD700"),
            ("🛏️ Номера", "rooms", "#FF6B35"),
            ("📊 Отчеты", "reports", "#00CED1")
        ]
        
        self.nav_buttons = {}
        for text, section, color in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda s=section: self.show_section(s),
                fg_color=color,
                hover_color=self.adjust_color(color, -30),
                height=45,
                font=ctk.CTkFont(size=15, weight="bold"),
                corner_radius=8
            )
            btn.pack(pady=8, fill="x")
            self.nav_buttons[section] = btn
        
        # Статистика
        self.create_sidebar_stats()
        
        # Переключатель темы
        theme_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_frame.pack(side="bottom", pady=20, padx=15, fill="x")
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame, 
            text="Тёмная тема", 
            command=self.toggle_theme,
            progress_color="#FFD700"
        )
        self.theme_switch.pack(pady=5, anchor="w")
        self.theme_switch.select()

    def create_sidebar_stats(self):
        """Создание блока статистики"""
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
        
        # Создаем фреймы для разных разделов
        self.hotels_frame = ctk.CTkFrame(self.main_content, corner_radius=0)
        self.rooms_frame = ctk.CTkFrame(self.main_content, corner_radius=0)
        self.reports_frame = ctk.CTkFrame(self.main_content, corner_radius=0)
        
        self.create_hotels_section()
        self.create_rooms_section()
        self.create_reports_section()
        
        # Показываем начальный раздел
        self.show_section("hotels")

    def create_hotels_section(self):
        """Создание раздела отелей"""
        # Верхняя панель
        top_panel = ctk.CTkFrame(self.hotels_frame, height=80, fg_color="#2a2a2a", corner_radius=0)
        top_panel.pack(fill="x")
        top_panel.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            top_panel,
            text="🏨 УПРАВЛЕНИЕ ОТЕЛЯМИ",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(side="left", padx=30, pady=25)
        
        # Кнопки управления
        actions_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        actions_frame.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(
            actions_frame,
            text="➕ Добавить отель",
            command=self.open_hotels_management,
            fg_color="#27ae60",
            hover_color="#219a52",
            width=140,
            height=35
        ).pack(side="left", padx=5)
        
        # Поиск и фильтры
        search_frame = ctk.CTkFrame(self.hotels_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=15)
        
        self.hotels_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Поиск отелей...",
            height=35
        )
        self.hotels_search_entry.pack(side="left", fill="x", expand=True)
        self.hotels_search_entry.bind("<KeyRelease>", lambda e: self.refresh_hotels_data())
        
        # Таблица отелей
        self.create_hotels_table()

    def create_rooms_section(self):
        """Создание раздела номеров"""
        top_panel = ctk.CTkFrame(self.rooms_frame, height=80, fg_color="#2a2a2a", corner_radius=0)
        top_panel.pack(fill="x")
        top_panel.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            top_panel,
            text="🛏️ УПРАВЛЕНИЕ НОМЕРАМИ",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FF6B35"
        )
        title_label.pack(side="left", padx=30, pady=25)
        
        actions_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        actions_frame.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(
            actions_frame,
            text="➕ Добавить номер",
            command=self.open_rooms_management,
            fg_color="#27ae60",
            hover_color="#219a52",
            width=140,
            height=35
        ).pack(side="left", padx=5)
        
        search_frame = ctk.CTkFrame(self.rooms_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=15)
        
        self.rooms_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Поиск номеров...",
            height=35
        )
        self.rooms_search_entry.pack(side="left", fill="x", expand=True)
        self.rooms_search_entry.bind("<KeyRelease>", lambda e: self.refresh_rooms_data())
        
        # Таблица номеров
        self.create_rooms_table()

    def create_reports_section(self):
        """Создание раздела отчетов"""
        top_panel = ctk.CTkFrame(self.reports_frame, height=80, fg_color="#2a2a2a", corner_radius=0)
        top_panel.pack(fill="x")
        top_panel.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            top_panel,
            text="📊 ОТЧЕТЫ И АНАЛИТИКА",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#00CED1"
        )
        title_label.pack(side="left", padx=30, pady=25)
        
        # Кнопки отчетов
        reports_buttons_frame = ctk.CTkFrame(self.reports_frame, fg_color="transparent")
        reports_buttons_frame.pack(pady=20)
        
        reports = [
            ("🏨 Статистика отелей", self.show_hotels_stats),
            ("🛏️ Статистика номеров", self.show_rooms_stats),
            ("💰 Анализ цен", self.show_pricing_stats)
        ]
        
        for text, command in reports:
            ctk.CTkButton(
                reports_buttons_frame,
                text=text,
                command=command,
                width=200,
                height=40,
                font=ctk.CTkFont(size=12)
            ).pack(pady=5)
        
        # Фрейм для графиков
        self.chart_frame = ctk.CTkFrame(self.reports_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def create_hotels_table(self):
        """Создание таблицы отелей"""
        columns = ("ID", "Отель", "Город", "Звезды", "Бассейн", "Номеров")
        
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Hotels.Treeview", 
                       background="#2a2d2e",
                       foreground="white",
                       fieldbackground="#2a2d2e",
                       rowheight=32)
        style.configure("Hotels.Treeview.Heading", 
                       background="#3b3b3b",
                       foreground="#FFD700",
                       relief="flat")
        style.map('Hotels.Treeview', background=[('selected', '#1f6aa5')])
        
        self.hotels_tree = ttk.Treeview(self.hotels_frame, columns=columns, show="headings", 
                                      style="Hotels.Treeview", height=15)
        
        column_config = {
            "ID": 70, "Отель": 250, "Город": 150, 
            "Звезды": 100, "Бассейн": 100, "Номеров": 100
        }
        
        for col in columns:
            self.hotels_tree.heading(col, text=col)
            self.hotels_tree.column(col, width=column_config[col])
        
        scrollbar = ttk.Scrollbar(self.hotels_frame, orient="vertical", command=self.hotels_tree.yview)
        self.hotels_tree.configure(yscrollcommand=scrollbar.set)
        
        self.hotels_tree.pack(fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)

    def create_rooms_table(self):
        """Создание таблицы номеров"""
        columns = ("ID", "Отель", "Номер", "Тип", "Цена", "Статус")
        
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Rooms.Treeview", 
                       background="#2a2d2e",
                       foreground="white",
                       fieldbackground="#2a2d2e",
                       rowheight=32)
        style.configure("Rooms.Treeview.Heading", 
                       background="#3b3b3b",
                       foreground="#FF6B35",
                       relief="flat")
        style.map('Rooms.Treeview', background=[('selected', '#1f6aa5')])
        
        self.rooms_tree = ttk.Treeview(self.rooms_frame, columns=columns, show="headings", 
                                     style="Rooms.Treeview", height=15)
        
        column_config = {
            "ID": 70, "Отель": 200, "Номер": 80, 
            "Тип": 120, "Цена": 120, "Статус": 100
        }
        
        for col in columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=column_config[col])
        
        scrollbar = ttk.Scrollbar(self.rooms_frame, orient="vertical", command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=scrollbar.set)
        
        self.rooms_tree.pack(fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)

    def show_section(self, section):
        """Показать выбранный раздел"""
        # Скрыть все разделы
        self.hotels_frame.pack_forget()
        self.rooms_frame.pack_forget()
        self.reports_frame.pack_forget()
        
        # Сбросить цвета кнопок
        for btn in self.nav_buttons.values():
            btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Показать выбранный раздел и подсветить кнопку
        if section == "hotels":
            self.hotels_frame.pack(fill="both", expand=True)
            self.nav_buttons["hotels"].configure(fg_color="#FFD700")
            self.refresh_hotels_data()
        elif section == "rooms":
            self.rooms_frame.pack(fill="both", expand=True)
            self.nav_buttons["rooms"].configure(fg_color="#FF6B35")
            self.refresh_rooms_data()
        elif section == "reports":
            self.reports_frame.pack(fill="both", expand=True)
            self.nav_buttons["reports"].configure(fg_color="#00CED1")
        
        self.current_section = section

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
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def refresh_data(self):
        """Обновление всех данных"""
        self.refresh_stats()
        if self.current_section == "hotels":
            self.refresh_hotels_data()
        elif self.current_section == "rooms":
            self.refresh_rooms_data()

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
        for item in self.hotels_tree.get_children():
            self.hotels_tree.delete(item)
        
        search_term = self.hotels_search_entry.get().lower() if hasattr(self, 'hotels_search_entry') else ""
        
        for hotel in self.hotel_vm.hotels:
            if search_term and (search_term not in hotel.name.lower() and 
                              search_term not in hotel.city.lower()):
                continue
            
            # Подсчет номеров в отеле
            room_count = sum(1 for room in self.room_vm.rooms if room.hotel_id == hotel.id)
            pool = "✅ Есть" if hotel.has_pool else "❌ Нет"
            stars_display = "⭐" * hotel.stars
            
            self.hotels_tree.insert("", "end", values=(
                hotel.id, hotel.name, hotel.city, stars_display, pool, room_count
            ))

    def refresh_rooms_data(self):
        """Обновление данных номеров"""
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)
        
        search_term = self.rooms_search_entry.get().lower() if hasattr(self, 'rooms_search_entry') else ""
        
        # Создаем словарь для быстрого доступа к отелям
        hotel_map = {hotel.id: hotel.name for hotel in self.hotel_vm.hotels}
        
        for room in self.room_vm.rooms:
            hotel_name = hotel_map.get(room.hotel_id, "Неизвестно")
            
            if search_term and (search_term not in room.room_number.lower() and 
                              search_term not in hotel_name.lower()):
                continue
            
            status = "✅ Доступен" if room.is_available else "❌ Занят"
            price = f"{room.price_per_night:,.0f} руб.".replace(",", " ")
            
            self.rooms_tree.insert("", "end", values=(
                room.id, hotel_name, room.room_number, room.room_type, price, status
            ))

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

    def show_hotels_stats(self):
        """Показать статистику отелей"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Анализ данных отелей
        cities = {}
        stars = {}
        
        for hotel in self.hotel_vm.hotels:
            # По городам
            if hotel.city not in cities:
                cities[hotel.city] = 0
            cities[hotel.city] += 1
            
            # По звездам
            if hotel.stars not in stars:
                stars[hotel.stars] = 0
            stars[hotel.stars] += 1
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Диаграмма по городам
        if cities:
            ax1.pie(cities.values(), labels=cities.keys(), autopct='%1.1f%%', startangle=90)
            ax1.set_title('Распределение отелей по городам')
        
        # Диаграмма по звездам
        if stars:
            star_labels = [f"{star}⭐" for star in sorted(stars.keys())]
            star_values = [stars[star] for star in sorted(stars.keys())]
            ax2.bar(star_labels, star_values, color=['gold', 'silver', 'brown', 'lightblue', 'lightgreen'])
            ax2.set_title('Распределение отелей по звездам')
            ax2.set_ylabel('Количество отелей')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_rooms_stats(self):
        """Показать статистику номеров"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Анализ данных номеров
        room_types = {}
        availability = {"Доступно": 0, "Занято": 0}
        
        for room in self.room_vm.rooms:
            # По типам номеров
            if room.room_type not in room_types:
                room_types[room.room_type] = 0
            room_types[room.room_type] += 1
            
            # По доступности
            if room.is_available:
                availability["Доступно"] += 1
            else:
                availability["Занято"] += 1
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Диаграмма по типам номеров
        if room_types:
            ax1.pie(room_types.values(), labels=room_types.keys(), autopct='%1.1f%%', startangle=90)
            ax1.set_title('Распределение номеров по типам')
        
        # Диаграмма по доступности
        if availability:
            ax2.pie(availability.values(), labels=availability.keys(), autopct='%1.1f%%', 
                   colors=['lightgreen', 'lightcoral'], startangle=90)
            ax2.set_title('Доступность номеров')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_pricing_stats(self):
        """Показать анализ цен"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Анализ цен по типам номеров
        prices_by_type = {}
        
        for room in self.room_vm.rooms:
            if room.room_type not in prices_by_type:
                prices_by_type[room.room_type] = []
            prices_by_type[room.room_type].append(room.price_per_night)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if prices_by_type:
            types = list(prices_by_type.keys())
            avg_prices = [sum(prices) / len(prices) for prices in prices_by_type.values()]
            min_prices = [min(prices) for prices in prices_by_type.values()]
            max_prices = [max(prices) for prices in prices_by_type.values()]
            
            x = range(len(types))
            width = 0.25
            
            ax.bar([i - width for i in x], min_prices, width, label='Мин. цена', color='lightgreen')
            ax.bar(x, avg_prices, width, label='Средняя цена', color='lightblue')
            ax.bar([i + width for i in x], max_prices, width, label='Макс. цена', color='lightcoral')
            
            ax.set_xlabel('Типы номеров')
            ax.set_ylabel('Цена (руб.)')
            ax.set_title('Анализ цен по типам номеров')
            ax.set_xticks(x)
            ax.set_xticklabels(types, rotation=45)
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

def main():
    json_service = JSONService()
    hotel_vm = HotelViewModel(json_service)
    room_vm = RoomViewModel(hotel_vm, json_service)

    app = CustomMainWindow(hotel_vm, room_vm)
    app.mainloop()

if __name__ == "__main__":
    main()