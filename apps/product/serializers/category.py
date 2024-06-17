from rest_framework.serializers import ValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer

from ..models import Category


class CategorySerializer(DocumentSerializer):
    class Meta:
        ref_name = "Category"
        model = Category
        fields = [
            "id",
            "name",
        ]

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

        user = self.context["request"].user

        name = attrs["name"]
        exists_name = False
        if self.instance:
            exists_name = Category.objects.filter(
                name__exact=name, id__ne=self.instance.id, registered_by=user
            ).count()
        else:
            exists_name = Category.objects.filter(
                name__exact=name, registered_by=user
            ).count()

        if exists_name:
            raise ValidationError({"error": "Este Nome já esta em uso!"})

        return attrs
