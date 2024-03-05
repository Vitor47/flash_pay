from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuditLog(models.Model):
    user = models.ForeignKey("userauth.User", on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"


class Log(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

        def __str__(self):
            content_object_str = str(self.content_object)
            if len(content_object_str) > 200:
                content_object_str = content_object_str[:197] + "..."

            return f"{content_object_str} ({self.action}) at {self.timestamp}"


class BaseModel(models.Model):
    cadastrado_por = models.ForeignKey(
        "userauth.User",
        related_name="%(class)s_cadastrado_por",
        on_delete=models.PROTECT,
    )
    editado_por = models.ForeignKey(
        "userauth.User",
        null=True,
        blank=True,
        related_name="%(class)s_editado_por",
        on_delete=models.PROTECT,
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
