class Hotel:
    """Класс, представляющий отель."""

    def __init__(self, id: int, name: str, city: str, address: str, stars: int, has_pool: bool = False):
        self.id = id
        self.name = name
        self.city = city
        self.address = address
        self.stars = stars
        self.has_pool = has_pool

    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "address": self.address,
            "stars": self.stars,
            "has_pool": self.has_pool
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря"""
        return cls(
            id=data["id"],
            name=data["name"],
            city=data["city"],
            address=data["address"],
            stars=data["stars"],
            has_pool=data["has_pool"]
        )

    def __repr__(self):
        pool = "с бассейном" if self.has_pool else "без бассейна"
        return f"Hotel(id={self.id}, name='{self.name}', city='{self.city}', address='{self.address}', stars={self.stars}, {pool})"