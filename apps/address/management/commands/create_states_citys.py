import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from apps.address.models import City, Country, State


class Command(BaseCommand):
    help = "Add states and citys with api viacep"

    def add_arguments(self, parser):
        parser.add_argument("--create_states", nargs="?", type=bool)

    def handle(self, *args, **options):
        options["create_states"]

        if State.objects.count() or City.objects.count():
            raise ValueError("Já existe dados de endereço salvos")

        pais = Country.objects.filter(name="brasil").first()
        estados_create = []
        for estado in State.state_choices.keys():
            estados_create.append(
                State(
                    name=estado,
                    country=pais,
                )
            )

        try:
            State.objects.insert(estados_create)
        except IntegrityError as error:
            raise CommandError(f"Erro ao criar os estados {error}")

        url = (
            f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/"
        )

        response = []
        try:
            response = requests.get(url)

            if response.status_code != 200:
                raise CommandError("Aconteceu um erro ao buscar as cidades")
        except requests.exceptions.RequestException:
            raise CommandError("Aconteceu um erro ao buscar as cidades")

        estados_cache = {estado.name: estado for estado in State.objects.all()}

        cidades_create = []
        cidades_response = response.json()
        for cidade in cidades_response:
            if cidade["nome"] in [cidade.name for cidade in cidades_create]:
                continue

            cidades_create.append(
                City(
                    name=cidade["nome"],
                    code_ibge=cidade["id"],
                    state=estados_cache[
                        cidade["microrregiao"]["mesorregiao"]["UF"]["sigla"]
                    ],
                )
            )

        try:
            City.objects.insert(cidades_create)
        except IntegrityError as error:
            raise CommandError(f"Erro ao criar as cidades {error}")

        self.stdout.write(
            self.style.SUCCESS("Estados e cidades adicionados com sucesso")
        )
