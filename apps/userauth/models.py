"""
This module allows importing AbstractBaseUser even when django.contrib.auth is
not in INSTALLED_APPS.
"""

import unicodedata
from datetime import datetime

from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    acheck_password,
    check_password,
    is_password_usable,
    make_password,
)
from django.utils.crypto import salted_hmac
from mongoengine import CASCADE, Document, fields

from apps.address.models import Address
from apps.log.models import BaseModel


class AbstractBaseUser:
    is_active = True

    REQUIRED_FIELDS = []

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def natural_key(self):
        return (self.full_name,)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    async def acheck_password(self, raw_password):
        """See check_password()."""

        async def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            await self.asave(update_fields=["password"])

        return await acheck_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        return self._get_session_auth_hash()

    def get_session_auth_fallback_hash(self):
        for fallback_secret in settings.SECRET_KEY_FALLBACKS:
            yield self._get_session_auth_hash(secret=fallback_secret)

    def _get_session_auth_hash(self, secret=None):
        key_salt = (
            "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        )
        return salted_hmac(
            key_salt,
            self.password,
            secret=secret,
            algorithm="sha256",
        ).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )


class User(AbstractBaseUser, BaseModel):
    sexo_choices = {
        "M": "Masculino",
        "F": "Feminino",
        "O": "Outro",
    }
    type_user_choices = {
        "vendedor": "Vendedor",
        "administrador": "Administrador",
        "aluno": "Aluno",
    }
    full_name = fields.StringField(max_length=250, required=True)
    email = fields.EmailField(required=True)
    telephone = fields.StringField(max_length=20, blank=True, null=True)
    rg = fields.StringField(max_length=20, blank=True, null=True)
    cpf_cnpj = fields.StringField(max_length=20, blank=True, null=True)
    birth_date = fields.DateField(blank=True, null=True)
    admin = fields.BooleanField(default=False)
    active = fields.BooleanField(default=True)
    type_user = fields.StringField(
        max_length=13,
        choices=type_user_choices.keys(),
        required=True,
        default="aluno",
    )
    sexo = fields.StringField(
        max_length=13,
        choices=sexo_choices.keys(),
        default="M",
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
