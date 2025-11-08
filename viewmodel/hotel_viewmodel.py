from typing import List, Callable
from model.hotel import Hotel
from service.json_service import JSONService

class HotelViewModel:
    def __init__(self, json_service: JSONService):
        self.json_service = json_service
        # Загрузка данных из JSON при инициализации
        self._hotels: List[Hotel] = self.json_service.load_data("hotels.json", Hotel)
        self._on_data_changed: Callable[[], None] = None

    @property
    def hotels(self) -> List[Hotel]:
        return self._hotels

    def set_on_data_changed(self, callback: Callable[[], None]):
        self._on_data_changed = callback

    def _notify(self):
        if self._on_data_changed:
            self._on_data_changed()

    def _save_data(self):
        """Сохранение данных в JSON файл"""
        self.json_service.save_data("hotels.json", self._hotels)

    def add_hotel(self, name: str, city: str, address: str, stars: int, has_pool: bool):
        if not name.strip():
            raise ValueError("Название отеля не может быть пустым.")

        if not city.strip():
            raise ValueError("Город не может быть пустым.")

        if not address.strip():
            raise ValueError("Адрес не может быть пустым.")

        if stars < 1 or stars > 5:
            raise ValueError("Количество звезд должно быть от 1 до 5.")

        # Проверка на уникальность названия в городе
        if any(h.name.lower() == name.strip().lower() and 
               h.city.lower() == city.strip().lower() for h in self._hotels):
            raise ValueError("Отель с таким названием в этом городе уже существует.")

        # Генерация нового ID
        new_id = max((h.id for h in self._hotels), default=0) + 1
        new_hotel = Hotel(new_id, name.strip(), city.strip(), address.strip(), stars, has_pool)
        self._hotels.append(new_hotel)
        self._save_data()
        self._notify()

    def update_hotel(self, hotel_id: int, name: str, city: str, address: str, stars: int, has_pool: bool):
        if not name.strip():
            raise ValueError("Название отеля не может быть пустым.")

        if not city.strip():
            raise ValueError("Город не может быть пустым.")

        if not address.strip():
            raise ValueError("Адрес не может быть пустым.")

        if stars < 1 or stars > 5:
            raise ValueError("Количество звезд должно быть от 1 до 5.")

        # Проверка на уникальность названия в городе (исключая текущий отель)
        if any(h.name.lower() == name.strip().lower() and 
               h.city.lower() == city.strip().lower() and 
               h.id != hotel_id for h in self._hotels):
            raise ValueError("Отель с таким названием в этом городе уже существует.")

        for hotel in self._hotels:
            if hotel.id == hotel_id:
                hotel.name = name.strip()
                hotel.city = city.strip()
                hotel.address = address.strip()
                hotel.stars = stars
                hotel.has_pool = has_pool
                self._save_data()
                self._notify()
                return
        raise ValueError(f"Отель с ID {hotel_id} не найден.")

    def delete_hotel(self, hotel_id: int):
        # Проверяем, есть ли номера в этом отеле
        from main import room_vm
        rooms_in_hotel = [room for room in room_vm.rooms if room.hotel_id == hotel_id]
        if rooms_in_hotel:
            raise ValueError("Нельзя удалить отель, в котором есть номера.")

        self._hotels = [h for h in self._hotels if h.id != hotel_id]
        self._save_data()
        self._notify()

    def get_hotel_by_id(self, hotel_id: int) -> Hotel:
        for hotel in self._hotels:
            if hotel.id == hotel_id:
                return hotel
        raise ValueError(f"Отель с ID {hotel_id} не найден.")