from mongoengine import fields

from apps.log.models import BaseModel


class Country(BaseModel):
    country_choices = {
        "brasil": "Brasil",
        "argentina": "Argentina",
        "bolivia": "Bolívia",
        "chile": "Chile",
        "colombia": "Colômbia",
        "paraguai": "Paraguai",
        "uruguai": "Uruguai",
        "venezuela": "Venezuela",
    }
    name = fields.StringField(
        max_length=20,
        choices=country_choices.keys(),
        default="Brasil",
        unique=True,
    )

    def __str__(self):
        return self.name

    meta = {"allow_inheritance": True}


class State(BaseModel):
    state_choices = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins",
    }
    name = fields.StringField(
        max_length=5,
        choices=state_choices.keys(),
        unique=True,
    )
    country = fields.ReferenceField(Country)

    def __str__(self):
        return self.name

    meta = {"allow_inheritance": True}


class City(BaseModel):
    name = fields.StringField(max_length=65, unique=True)
    code_ibge = fields.StringField(
        max_length=7,
        null=True,
        blank=True,
        unique=True,
    )
    state = fields.ReferenceField(State)

    def __str__(self):
        return f"{self.name} {self.state}"

    meta = {"allow_inheritance": True}


class Address(BaseModel):
    cep = fields.StringField(max_length=8)
    neighborhood = fields.StringField(max_length=200, null=True, blank=True)
    street = fields.StringField(max_length=200)
    house_number = fields.IntField(null=True, blank=True)
    complement = fields.StringField(max_length=200, null=True, blank=True)
    city = fields.ReferenceField(City)
    state = fields.ReferenceField(State)
    country = fields.ReferenceField(Country)

    def __str__(self):
        return f"{self.cep} {self.street}"

    meta = {"allow_inheritance": True}

    @property
    def country_object(self):
        if self.country:
            return {
                "id": self.country.id,
                "name": self.country.name,
            }
        return None

    @property
    def state_object(self):
        if self.state:
            return {
                "id": self.state.id,
                "name": self.state.name,
            }
        return None

    @property
    def city_object(self):
        if self.city:
            return {
                "id": self.city.id,
                "name": self.city.name,
                "ibge_code": self.city.ibge_code,
            }
        return None
