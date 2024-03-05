from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.log.models import AuditLog, Log


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Cria um registro de auditoria para cada login bem-sucedido no sistema.
    """

    ip_address = request.META.get("REMOTE_ADDR")
    AuditLog.objects.create(user=user, ip_address=ip_address)


@receiver(post_save)
def log_create_or_update(sender, instance, created, **kwargs):
    """
    Cria um registro de log para cada objeto criado ou atualizado no sistema.
    """
    # Ignora os registros de log para evitar recursão infinita.
    if sender == Log:
        return

    # Verifica se o objeto é rastreável.
    try:
        content_type = ContentType.objects.get_for_model(sender)
    except:
        return

    if (
        not content_type.app_label == "core"
        and not content_type.app_label == "endereco"
    ):
        return

    # Cria o registro de log.
    if created:
        action = "create"
    else:
        action = "update"

    Log.objects.create(
        content_type=content_type,
        object_id=instance.id,
        action=action,
        object_repr=str(instance),
    )


@receiver(pre_delete)
def log_delete(sender, instance, **kwargs):
    """
    Cria um registro de log para cada objeto excluído no sistema.
    """
    # Ignora os registros de log para evitar recursão infinita.
    if sender == Log:
        return

    # Verifica se o objeto é rastreável.
    try:
        content_type = ContentType.objects.get_for_model(sender)
    except:
        return

    if (
        not content_type.app_label == "core"
        and not content_type.app_label == "endereco"
    ):
        return

    # Cria o registro de log.
    Log.objects.create(
        content_type=content_type,
        object_id=instance.id,
        action="delete",
        object_repr=str(instance),
    )
