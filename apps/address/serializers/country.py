# -*- coding: utf-8 -*-
from rest_framework.serializers import ValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer

from apps.address.models import Country


class UniversitySerializer(DocumentSerializer):
    class Meta:
        ref_name = "University"
        model = Country
        fields = ["id", "name"]

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

        name = attrs.get("name", None)
        exists_name = False
        if self.instance:
            exists_name = Country.objects.filter(
                name__exact=name, id__ne=self.instance.id
            ).count()
        else:
            exists_name = Country.objects.filter(name__exact=name).count()

        if exists_name:
            raise ValidationError({"error": "Este nome já esta em uso!"})

        return attrs
