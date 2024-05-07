from datetime import datetime

from django.conf import settings
from mongoengine import Document, fields


class OutstandingToken(Document):
    user = fields.ReferenceField(
        settings.USER_MODEL_MONGO,
        null=True,
        blank=True,
    )

    jti = fields.StringField(unique=True, max_length=255)
    token = fields.StringField()

    created_at = fields.DateTimeField(null=True, blank=True)
    expires_at = fields.DateTimeField()

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = (
            "rest_framework_simplejwt.token_blacklist"
            not in settings.INSTALLED_APPS
        )
        ordering = ("user",)

    def __str__(self) -> str:
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class BlacklistedToken(Document):
    token = fields.ReferenceField(
        OutstandingToken,
    )

    blacklisted_at = fields.DateTimeField(default=datetime.now())

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = (
            "rest_framework_simplejwt.token_blacklist"
            not in settings.INSTALLED_APPS
        )

    def __str__(self) -> str:
        return f"Blacklisted token for {self.token.user}"
