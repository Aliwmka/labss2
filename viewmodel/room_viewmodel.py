from typing import List, Callable
from model.room import Room
from service.json_service import JSONService

class RoomViewModel:
    def __init__(self, hotel_vm, json_service: JSONService):
        self.hotel_vm = hotel_vm
        self.json_service = json_service
        # Загрузка данных из JSON при инициализации
        self._rooms: List[Room] = self.json_service.load_data("rooms.json", Room)
        self._on_data_changed: Callable[[], None] = None

    @property
    def rooms(self) -> List[Room]:
        return self._rooms

    def set_on_data_changed(self, callback: Callable[[], None]):
        self._on_data_changed = callback

    def _notify(self):
        if self._on_data_changed:
            self._on_data_changed()

    def _save_data(self):
        """Сохранение данных в JSON файл"""
        self.json_service.save_data("rooms.json", self._rooms)

    def add_room(self, hotel_id: int, room_number: str, room_type: str, price_per_night: float, is_available: bool = True):
        if not room_number.strip():
            raise ValueError("Номер комнаты не может быть пустым.")

        if not room_type.strip():
            raise ValueError("Тип номера не может быть пустым.")

        if price_per_night <= 0:
            raise ValueError("Цена за ночь должна быть положительной.")

        # Проверяем существование отеля
        hotel_exists = any(h.id == hotel_id for h in self.hotel_vm.hotels)
        if not hotel_exists:
            raise ValueError("Указанный отель не существует.")

        # Проверка на уникальность номера комнаты в отеле
        if any(r.room_number == room_number.strip() and 
               r.hotel_id == hotel_id for r in self._rooms):
            raise ValueError("Номер с таким названием уже существует в этом отеле.")

        # Генерация нового ID
        new_id = max((r.id for r in self._rooms), default=0) + 1
        new_room = Room(new_id, hotel_id, room_number.strip(), room_type.strip(), price_per_night, is_available)
        self._rooms.append(new_room)
        self._save_data()
        self._notify()

    def update_room(self, room_id: int, hotel_id: int, room_number: str, room_type: str, price_per_night: float, is_available: bool):
        if not room_number.strip():
            raise ValueError("Номер комнаты не может быть пустым.")

        if not room_type.strip():
            raise ValueError("Тип номера не может быть пустым.")

        if price_per_night <= 0:
            raise ValueError("Цена за ночь должна быть положительной.")

        # Проверяем существование отеля
        hotel_exists = any(h.id == hotel_id for h in self.hotel_vm.hotels)
        if not hotel_exists:
            raise ValueError("Указанный отель не существует.")

        # Проверка на уникальность номера комнаты в отеле (исключая текущий номер)
        if any(r.room_number == room_number.strip() and 
               r.hotel_id == hotel_id and 
               r.id != room_id for r in self._rooms):
            raise ValueError("Номер с таким названием уже существует в этом отеле.")

        for room in self._rooms:
            if room.id == room_id:
                room.hotel_id = hotel_id
                room.room_number = room_number.strip()
                room.room_type = room_type.strip()
                room.price_per_night = price_per_night
                room.is_available = is_available
                self._save_data()
                self._notify()
                return
        raise ValueError(f"Номер с ID {room_id} не найден.")

    def delete_room(self, room_id: int):
        self._rooms = [r for r in self._rooms if r.id != room_id]
        self._save_data()
        self._notify()

    def get_room_by_id(self, room_id: int) -> Room:
        for room in self._rooms:
            if room.id == room_id:
                return room
        raise ValueError(f"Номер с ID {room_id} не найден.")