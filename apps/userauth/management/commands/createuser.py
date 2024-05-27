from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from apps.userauth.models import User


class Command(BaseCommand):
    help = "Create random user"

    def add_arguments(self, parser):
        parser.add_argument(
            "-a", "--is_admin", type=bool, help="Create an admin account?"
        )

    def handle(self, *args, **kwargs):
        admin = kwargs["is_admin"]

        password = make_password("root")

        dict_type_user = {
            True: "administrador",
            False: "aluno",
        }

        if User.objects.filter(
            email="root@root.com",
        ).first():
            raise ValueError("Já existe um superuser com esse e-mail")

        user = User(
            full_name="Root",
            email="root@root.com",
            sexo="M",
            admin=admin,
            type_user=dict_type_user[admin],
            password=password,
        )
        user.save()
