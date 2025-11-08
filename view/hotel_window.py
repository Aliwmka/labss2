import tkinter as tk
from tkinter import ttk, messagebox
from view.new_hotel_window import NewHotelWindow

class HotelWindow(tk.Toplevel):
    def __init__(self, parent, view_model):
        super().__init__(parent)
        self.title("Отели")
        self.geometry("800x450")
        self.vm = view_model
        self.vm.set_on_data_changed(self.refresh_table)

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Добавить", command=self.add_hotel).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_hotel).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_hotel).pack(side="left", padx=5)

        # Таблица
        columns = ("ID", "Название", "Город", "Адрес", "Звезды", "Бассейн")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=50)
        self.tree.column("Название", width=150)
        self.tree.column("Город", width=120)
        self.tree.column("Адрес", width=200)
        self.tree.column("Звезды", width=80)
        self.tree.column("Бассейн", width=80)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def refresh_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Заполнение
        for hotel in self.vm.hotels:
            pool = "Да" if hotel.has_pool else "Нет"
            self.tree.insert("", "end", values=(
                hotel.id, hotel.name, hotel.city, hotel.address, hotel.stars, pool
            ))

    def get_selected_id(self):
        sel = self.tree.selection()
        return int(self.tree.item(sel[0])["values"][0]) if sel else None

    def add_hotel(self):
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
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_hotel(self):
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
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_hotel(self):
        hotel_id = self.get_selected_id()
        if not hotel_id:
            messagebox.showwarning("Внимание", "Выберите отель для удаления.")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить отель?"):
            try:
                self.vm.delete_hotel(hotel_id)
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))