from mongoengine import CASCADE, fields

from apps.core.models import Shoppe, University
from apps.log.models import BaseModel


class Category(BaseModel):
    name = fields.StringField()

    meta = {"allow_inheritance": True}

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    name = fields.StringField(max_length=500)
    price = fields.DecimalField(default=0, required=True)
    image = fields.ImageField(required=True)
    category = fields.ReferenceField(
        Category, reverse_delete_rule=CASCADE, required=True
    )
    shoppe = fields.ReferenceField(
        Shoppe, reverse_delete_rule=CASCADE, required=True
    )
    university = fields.ReferenceField(
        University, reverse_delete_rule=CASCADE, required=True
    )
    description = fields.StringField(required=True)
    quantity = fields.DecimalField(default=0, required=True)

    meta = {"allow_inheritance": True}

    def __str__(self) -> str:
        return self.name

    @property
    def category_dict(self):
        return {
            "id": self.category._id,
            "name": self.category.name,
        }

    @property
    def university_dict(self):
        return {
            "id": self.university._id,
            "name": self.university.name,
        }
