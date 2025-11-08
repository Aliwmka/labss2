from view.main_window import MainWindow
from viewmodel.hotel_viewmodel import HotelViewModel
from viewmodel.room_viewmodel import RoomViewModel
from service.json_service import JSONService

def main():
    # Создание сервиса для работы с JSON
    json_service = JSONService()

    # Создание ViewModel с передачей JSON сервиса
    hotel_vm = HotelViewModel(json_service)
    room_vm = RoomViewModel(hotel_vm, json_service)

    # Глобальные переменные для доступа между ViewModel
    import builtins
    builtins.hotel_vm = hotel_vm
    builtins.room_vm = room_vm

    # Запуск приложения
    app = MainWindow(hotel_vm, room_vm)
    app.mainloop()

if __name__ == "__main__":
    main()