from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from apps.log.models import BaseModel

from .managers import UserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Usuario(BaseModel):
    class SexoChoices(models.TextChoices):
        FEMININO = "F", "Feminino"
        MASCULINO = "M", "Masculino"
        OUTRO = "O", "Outro"

    # dados pessoais
    nome_completo = models.CharField(
        "Nome completo", max_length=250, blank=True
    )
    telefone = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    sexo = models.CharField(
        "Sexo",
        max_length=1,
        choices=SexoChoices.choices,
        help_text="Sexo do usuário",
    )
    pertence_amf = models.BooleanField(default=True)
    endereco = models.ForeignKey(
        "endereco.Endereco",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class RevokedToken(models.Model):
    key = models.CharField("Key", max_length=500, unique=True)
    user = models.ForeignKey(
        User, related_name="token_user", on_delete=models.CASCADE
    )
    revoked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Revoked Token JWT"
        verbose_name_plural = "Revokeds Tokens JWT"

    def __str__(self) -> str:
        return "Revoked Token"

    @classmethod
    def create_revoked_token(cls, user_id, token: str) -> dict:
        return cls.objects.create(user_id=user_id, key=str(token))
