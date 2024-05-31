from base64 import b64encode

from rest_framework.serializers import ValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer

from apps.core.utils import format_cpf_cnpj, is_cnpj_valid, only_numbers

from ..models import Shoppe


class ShoppeSerializer(DocumentSerializer):
    class Meta:
        ref_name = "Shoppe"
        model = Shoppe
        fields = ["id", "name", "cnpj", "image"]

    def create(self, validated_data):
        try:
            validated_data["registered_by"] = self.context["request"].user
            return super().create(validated_data)
        except Exception as error:
            raise ValidationError({"detail": error})

    def update(self, instance, validated_data):
        try:
            validated_data["edited_by"] = self.context["request"].user
            return super().update(instance, validated_data)
        except Exception as error:
            raise ValidationError({"detail": error})

    def validate(self, attrs):
        attrs = super().validate(attrs)

        cnpj = only_numbers(attrs.get("cnpj", ""))
        if cnpj:
            if len(cnpj) == 14:
                validated_cnpj = is_cnpj_valid(cnpj)
                if not validated_cnpj:
                    raise ValidationError({"error": "CNPJ inválido!"})
            else:
                raise ValidationError({"error": "CPF ou CNPJ inválido!"})

            exists_cnpj = False
            if self.instance:
                exists_cnpj = Shoppe.objects.filter(
                    cnpj__exact=cnpj, id__ne=self.instance.id
                ).count()
            else:
                exists_cnpj = Shoppe.objects.filter(cnpj__exact=cnpj).count()

            if exists_cnpj:
                raise ValidationError({"error": "Este CNPJ já esta em uso!"})

            attrs["cnpj"] = cnpj

        return attrs

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["cnpj"] = format_cpf_cnpj(instance["cnpj"])

        image_id = instance["image"]
        if not image_id:
            return instance

        try:
            shoppe_db = Shoppe.objects.get(id=instance["id"])
            image_data = shoppe_db.image.read()
            instance["image"] = b64encode(image_data).decode("utf-8")
        except:
            pass

        return instance
