from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

from django.contrib.auth import models as auth_models
from django.db.models.manager import EmptyManager
from django.utils.functional import cached_property
from mongoengine import CASCADE, Document, fields
from rest_framework_simplejwt.settings import api_settings

from apps.log.models import BaseModel
from apps.userauth.models import User

if TYPE_CHECKING:
    from .token.tokens import Token


class TokenUser:
    """
    A dummy user class modeled after django.contrib.auth.models.AnonymousUser.
    Used in conjunction with the `JWTStatelessUserAuthentication` backend to
    implement single sign-on functionality across services which share the same
    secret key.  `JWTStatelessUserAuthentication` will return an instance of this
    class instead of a `User` model instance.  Instances of this class act as
    stateless user objects which are backed by validated tokens.
    """

    # User is always active since Simple JWT will never issue a token for an
    # inactive user
    active = True

    _groups = EmptyManager(auth_models.Group)
    _user_permissions = EmptyManager(auth_models.Permission)

    def __init__(self, token: "Token") -> None:
        self.token = token

    def __str__(self) -> str:
        return f"TokenUser {self.id}"

    @cached_property
    def id(self) -> Union[int, str]:
        return self.token[api_settings.USER_ID_CLAIM]

    @cached_property
    def pk(self) -> Union[int, str]:
        return self.id

    @cached_property
    def full_name(self) -> str:
        return self.token.get("full_name", "")

    @cached_property
    def admin(self) -> bool:
        return self.token.get("admin", False)

    @cached_property
    def super_admin(self) -> bool:
        return self.token.get("super_admin", False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenUser):
            return NotImplemented
        return self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.id)

    def save(self) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def delete(self) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def set_password(self, raw_password: str) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def check_password(self, raw_password: str) -> None:
        raise NotImplementedError("Token users have no DB representation")

    @property
    def groups(self) -> auth_models.Group:
        return self._groups

    @property
    def user_permissions(self) -> auth_models.Permission:
        return self._user_permissions

    def get_group_permissions(self, obj: Optional[object] = None) -> set:
        return set()

    def get_all_permissions(self, obj: Optional[object] = None) -> set:
        return set()

    def has_perm(self, perm: str, obj: Optional[object] = None) -> bool:
        return False

    def has_perms(
        self, perm_list: List[str], obj: Optional[object] = None
    ) -> bool:
        return False

    def has_module_perms(self, module: str) -> bool:
        return False

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_authenticated(self) -> bool:
        return True

    def get_email(self) -> str:
        return self.email

    def __getattr__(self, attr: str) -> Optional[Any]:
        """This acts as a backup attribute getter for custom claims defined in Token serializers."""
        return self.token.get(attr, None)


class RevokedToken(Document):
    key = fields.StringField(max_length=500, unique=True)
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE)
    revoked_at = fields.DateTimeField(default=datetime.now)

    meta = {"allow_inheritance": True}

    def __str__(self) -> str:
        return "Revoked Token"

    @classmethod
    def create_revoked_token(cls, user_id, token: str) -> dict:
        return cls.objects.create(user=user_id, key=str(token))


class University(Document):
    name = fields.StringField(max_length=500, unique=True)
    cnpj = fields.StringField(max_length=14, unique=True)

    meta = {"allow_inheritance": True}

    def __str__(self) -> str:
        return self.name


class Shoppe(BaseModel):
    name = fields.StringField(max_length=500, required=True)
    cnpj = fields.StringField(
        max_length=14,
        required=True,
    )
    description = fields.StringField()
    image = fields.ImageField()
    university = fields.ReferenceField(University, required=True)

    meta = {"allow_inheritance": True}

    def __str__(self) -> str:
        return self.name

    @property
    def image_url(self):
        return self.image.grid_id
