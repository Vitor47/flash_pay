from rest_framework.serializers import ValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer

from apps.core.utils import format_cpf_cnpj, is_cnpj_valid, only_numbers

from ..models import University


class UniversitySerializer(DocumentSerializer):
    class Meta:
        ref_name = "University"
        model = University
        fields = ["id", "name", "cnpj"]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        cnpj = only_numbers(attrs.get("cnpj", ""))

        if len(cnpj) == 14:
            validated_cnpj = is_cnpj_valid(cnpj)
            if not validated_cnpj:
                raise ValidationError({"error": "CNPJ inválido!"})
        else:
            raise ValidationError({"error": "CPF ou CNPJ inválido!"})

        exists_cnpj = False
        if self.instance:
            exists_cnpj = University.objects.filter(
                cnpj__exact=cnpj, id__ne=self.instance.id
            ).count()
        else:
            exists_cnpj = University.objects.filter(cnpj__exact=cnpj).count()

        if exists_cnpj:
            raise ValidationError({"error": "Este CNPJ já esta em uso!"})

        attrs["cnpj"] = cnpj

        name = attrs.get("name", None)
        exists_name = False
        if self.instance:
            exists_name = University.objects.filter(
                name__exact=name, id__ne=self.instance.id
            ).count()
        else:
            exists_name = University.objects.filter(name__exact=name).count()

        if exists_name:
            raise ValidationError({"error": "Este nome já esta em uso!"})

        return attrs

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["cnpj"] = format_cpf_cnpj(instance["cnpj"])
        return instance
