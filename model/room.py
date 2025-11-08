class Room:
    """Класс, представляющий номер в отеле."""

    def __init__(self, id: int, hotel_id: int, room_number: str, room_type: str, price_per_night: float, is_available: bool = True):
        self.id = id
        self.hotel_id = hotel_id
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = is_available

    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "room_number": self.room_number,
            "room_type": self.room_type,
            "price_per_night": self.price_per_night,
            "is_available": self.is_available
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря"""
        return cls(
            id=data["id"],
            hotel_id=data["hotel_id"],
            room_number=data["room_number"],
            room_type=data["room_type"],
            price_per_night=data["price_per_night"],
            is_available=data["is_available"]
        )

    def __repr__(self):
        status = "доступен" if self.is_available else "занят"
        return f"Room(id={self.id}, hotel_id={self.hotel_id}, room_number='{self.room_number}', type='{self.room_type}', price={self.price_per_night}, status='{status}')"