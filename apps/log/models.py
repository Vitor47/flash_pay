from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from mongoengine import Document, fields
from datetime import datetime


class AuditLog(Document):
    user = fields.ReferenceField("userauth.User")
    login_time = fields.DateTimeField(default=datetime.now())
    ip_address = fields.BinaryField()

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"


class Log(Document):
    object_id = fields.IntField(min_value=1)
    action = fields.StringField(max_length=50)
    timestamp = fields.DateTimeField(default=datetime.now())
    object_repr = fields.StringField(blank=True, null=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

        def __str__(self):
            content_object_str = str(self.content_object)
            if len(content_object_str) > 200:
                content_object_str = content_object_str[:197] + "..."

            return f"{content_object_str} ({self.action}) at {self.timestamp}"


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

    meta = {'allow_inheritance': True}
