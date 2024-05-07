from datetime import datetime

from mongoengine import Document, fields


class AuditLog(Document):
    user = fields.ReferenceField("userauth.User")
    login_time = fields.DateTimeField(default=datetime.now())
    ip_address = fields.StringField()

    meta = {"allow_inheritance": True}


class Log(Document):
    object_id = fields.IntField(min_value=1)
    action = fields.StringField(max_length=50)
    timestamp = fields.DateTimeField(default=datetime.now())
    object_repr = fields.StringField(blank=True, null=True)

    meta = {"allow_inheritance": True}


class BaseModel(Document):
    cadastrado_por = fields.ReferenceField(
        "userauth.User",
        related_name="%(class)s_cadastrado_por",
    )
    editado_por = fields.ReferenceField(
        "userauth.User",
        null=True,
        blank=True,
        related_name="%(class)s_editado_por",
    )
    data_cadastro = fields.DateTimeField(default=datetime.now())
    data_alteracao = fields.DateTimeField(default=datetime.now())

    meta = {"allow_inheritance": True}
