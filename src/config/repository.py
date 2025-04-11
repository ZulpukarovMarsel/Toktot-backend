
from django.db.models import Model, QuerySet

from typing import Type, Optional


class BaseRepository:
    """
    Базовый репозиторий для работы с моделями Django.

    Этот класс предоставляет общие методы для выполнения CRUD-операций
    (создание, чтение, обновление, удаление) с моделями Django.
    """
    model: Type[Model] = None

    @classmethod
    def get_all(cls) -> QuerySet:
        """
        Возвращает все объекты модели.
        """
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, obj_id: int) -> Optional[Model]:
        """
        Возвращает объект модели по его ID.
        """
        return cls.model.objects.filter(id=obj_id).first()

    @classmethod
    def get_by_slug(cls, slug: str) -> Optional[Model]:
        """
        Возвращает объект модели по его slug.
        """
        return cls.model.objects.filter(slug=slug).first()

    @classmethod
    def create(cls, data: dict) -> Model:
        """
        Создает новый объект модели.
        """
        return cls.model.objects.create(**data)

    @classmethod
    def update(cls, obj: Model, data: dict) -> Model:
        """
        Обновляет существующий объект модели.
        """
        for attr, value in data.items():
            setattr(obj, attr, value)
        obj.save()
        return obj

    @classmethod
    def delete(cls, obj: Model) -> None:
        """
        Удаляет объект модели.
        """
        obj.delete()
