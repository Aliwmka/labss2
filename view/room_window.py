import tkinter as tk
from tkinter import ttk, messagebox
from view.new_room_window import NewRoomWindow

class RoomWindow(tk.Toplevel):
    def __init__(self, parent, room_vm, hotel_vm):
        super().__init__(parent)
        self.title("Номера")
        self.geometry("900x450")
        self.room_vm = room_vm
        self.hotel_vm = hotel_vm
        self.room_vm.set_on_data_changed(self.refresh_table)

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Добавить", command=self.add_room).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_room).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_room).pack(side="left", padx=5)

        # Таблица
        columns = ("ID", "Отель", "Номер", "Тип", "Цена за ночь", "Статус")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=50)
        self.tree.column("Отель", width=150)
        self.tree.column("Номер", width=80)
        self.tree.column("Тип", width=100)
        self.tree.column("Цена за ночь", width=120)
        self.tree.column("Статус", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def refresh_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Создаём словарь ID → название отеля
        hotel_map = {hotel.id: f"{hotel.name} ({hotel.city})" for hotel in self.hotel_vm.hotels}
        
        # Заполнение
        for room in self.room_vm.rooms:
            status = "Доступен" if room.is_available else "Занят"
            hotel_name = hotel_map.get(room.hotel_id, "Неизвестно")
            self.tree.insert("", "end", values=(
                room.id, hotel_name, room.room_number, room.room_type, 
                f"{room.price_per_night:.2f} руб.", status
            ))

    def get_selected_id(self):
        sel = self.tree.selection()
        return int(self.tree.item(sel[0])["values"][0]) if sel else None

    def add_room(self):
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
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_room(self):
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
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_room(self):
        room_id = self.get_selected_id()
        if not room_id:
            messagebox.showwarning("Внимание", "Выберите номер для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить номер?"):
            try:
                self.room_vm.delete_room(room_id)
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))