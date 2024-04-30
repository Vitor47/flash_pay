from datetime import datetime

from mongoengine import CASCADE, Document, fields

from apps.address.models import Address
from apps.log.models import BaseModel


class User(BaseModel):
    sexo_choices = {
        "M": "Masculino",
        "F": "Feminino",
        "O": "Outro",
    }
    full_name = fields.StringField(max_length=250, required=True)
    email = fields.EmailField(required=True)
    telephone = fields.StringField(max_length=20, blank=True, null=True)
    rg = fields.StringField(max_length=20, blank=True, null=True)
    cpf_cnpj = fields.StringField(max_length=20, blank=True, null=True)
    birth_date = fields.DateField(blank=True, null=True)
    sexo = fields.StringField(
        max_length=1, choices=sexo_choices.keys(), required=True
    )
    address = fields.ReferenceField(
        Address, required=True, reverse_delete_rule=CASCADE
    )
    password = fields.StringField(required=True)

    meta = {"allow_inheritance": True}


class RevokedToken(Document):
    key = fields.StringField(max_length=500, unique=True)
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE)
    revoked_at = fields.DateTimeField(default=datetime.now)

    meta = {"allow_inheritance": True}

    def __str__(self) -> str:
        return "Revoked Token"

    @classmethod
    def create_revoked_token(cls, user_id, token: str) -> dict:
        return cls.objects.create(user_id=user_id, key=str(token))
