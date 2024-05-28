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
    registered_by = fields.ReferenceField(
        "userauth.User",
        related_name="%(class)s_registered_by",
    )
    edited_by = fields.ReferenceField(
        "userauth.User",
        null=True,
        blank=True,
        related_name="%(class)s_edited_by",
    )
    registration_date = fields.DateTimeField(default=datetime.now())
    modification_date = fields.DateTimeField(default=datetime.now())

    meta = {"allow_inheritance": True}
