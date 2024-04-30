from mongoengine import fields
from rest_framework_mongoengine.serializers import DocumentSerializer

from ..models import Address


class AddressRetrieveSerializer(DocumentSerializer):
    country = fields.DictField(source="country_object")
    state = fields.DictField(source="state_object")
    city = fields.DictField(source="city_object")

    class Meta:
        model = Address
        fields = [
            "id",
            "cep",
            "neighborhood",
            "street",
            "house_number",
            "complement",
            "city",
            "state",
            "country",
        ]
