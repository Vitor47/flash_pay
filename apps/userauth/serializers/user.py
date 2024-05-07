from django.contrib.auth.hashers import make_password
from mongoengine import fields
from rest_framework.serializers import ValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer

from apps.address.models import Address
from apps.address.serializers.address import AddressRetrieveSerializer
from apps.core.utils import (
    format_cpf_cnpj,
    is_cnpj_valid,
    is_cpf_valid,
    is_email_valid,
    is_password_valid,
    only_numbers,
)

from ..models import User


class AddressSerializer(DocumentSerializer):
    class Meta:
        ref_name = "Address"
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


class UserSerializer(DocumentSerializer):
    address = AddressSerializer()

    class Meta:
        ref_name = "User"
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "telephone",
            "rg",
            "cpf_cnpj",
            "birth_date",
            "sexo",
            "address",
            "admin",
            "type_user",
            "password",
        ]

    def create(self, validated_data):
        if validated_data.get("address"):
            address = validated_data.pop("address")
            validated_data["address"] = Address.objects.create(**address).id

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        addres = validated_data.pop("addres")

        if addres:
            Address.objects.filter(id=instance.id).update(**addres)

        return User.objects.filter(id=instance.id).update(**validated_data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user

        if attrs.get("type_user") == "aluno" and not attrs.get("admin"):
            pass
        elif user.is_authenticated:
            if attrs.get("admin") and not user.admin:
                raise ValidationError(
                    {
                        "error": (
                            "Você não tem permissão para criar um"
                            " Administrador."
                        )
                    }
                )
            if attrs.get("type_user") != "aluno" and not user.admin:
                raise ValidationError(
                    {
                        "error": (
                            "Você não tem permissão para criar um Usuário não"
                            " aluno."
                        )
                    }
                )
        else:
            raise ValidationError(
                {"error": "Você não tem permissão para essa ação."}
            )

        if attrs.get("cpf_cnpj", ""):
            cpf_cnpj = only_numbers(attrs.get("cpf_cnpj", ""))
            if self.instance:
                exists_cpf_cnpj = (
                    User.objects.filter(cpf_cnpj__exact=cpf_cnpj)
                    .exclude(id=self.instance.id)
                    .count()
                )
            else:
                exists_cpf_cnpj = User.objects.filter(
                    cpf_cnpj__exact=cpf_cnpj
                ).count()

            if exists_cpf_cnpj:
                raise ValidationError(
                    {"error": "Este cpf ou cnpj já esta em uso!"}
                )

            if len(cpf_cnpj) == 11:
                validated_cepf = is_cpf_valid(cpf_cnpj)
                if not validated_cepf:
                    raise ValidationError({"error": "CPF inválido!"})

            elif len(cpf_cnpj) == 14:
                validated_cepf = is_cnpj_valid(cpf_cnpj)
                if not validated_cepf:
                    raise ValidationError({"error": "CNPJ inválido!"})
            else:
                raise ValidationError({"error": "CPF ou CNPJ inválido!"})

            attrs["cpf_cnpj"] = cpf_cnpj

        email = attrs.get("email", None)
        exists_email = False
        if self.instance:
            exists_email = (
                User.objects.filter(email__exact=email)
                .exclude(id=self.instance.id)
                .count()
            )
        else:
            exists_email = User.objects.filter(email__exact=email).count()

        if exists_email:
            raise ValidationError({"error": "Este e-mail já esta em uso!"})

        validated_email = is_email_valid(email)
        if not validated_email:
            raise ValidationError({"error": "E-mail inválido!"})

        if not self.instance or "password" in attrs:
            password = attrs.get("password", None)
            if not password:
                raise ValidationError({"error": "A senha é obrigatória."})

            if not is_password_valid(password):
                raise ValidationError({"error": "A senha não é válida."})

            attrs["password"] = make_password(password)

        return attrs


class UsuarioRetrieveMixinSerializer(DocumentSerializer):
    id = fields.IntField()
    cpf_cnpj = fields.StringField(required=True)
    full_name = fields.StringField(required=True)
    email = fields.EmailField(required=True)
    birth_date = fields.DateField(required=True)
    address = AddressRetrieveSerializer(many=False, required=True)
    type_user = fields.StringField(db_field="get_type_user_display")

    class Meta:
        model = User
        ref_name = "User"
        fields = [
            "id",
            "full_name",
            "email",
            "birth_date",
            "telephone",
            "rg",
            "cpf_cnpj",
            "address",
            "admin",
            "type_user",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["cpf_cnpj"] = (
            format_cpf_cnpj(representation["cpf_cnpj"])
            if representation["cpf_cnpj"]
            else None
        )
        return representation
