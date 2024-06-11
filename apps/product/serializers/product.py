from base64 import b64encode

from rest_framework.serializers import ValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer

from apps.core.serializers.university import UniversitySerializer

from ..models import Product
from ..serializers.category import CategorySerializer


class ProductSerializer(DocumentSerializer):
    class Meta:
        ref_name = "Product"
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "description",
            "price",
            "category",
            "university",
            "quantity",
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

    def to_representation(self, instance):
        instance = super().to_representation(instance)

        image_id = instance["image"]
        if not image_id:
            return instance

        try:
            product_db = Product.objects.get(id=instance["id"])
            image_data = product_db.image.read()
            instance["image"] = b64encode(image_data).decode("utf-8")
        except:
            pass

        return instance


class ProductRetrieveSerializer(DocumentSerializer):
    category = CategorySerializer(many=False)
    university = UniversitySerializer(many=False)

    class Meta:
        ref_name = "Product"
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "description",
            "price",
            "category",
            "university",
            "quantity",
        ]

    def to_representation(self, instance):
        instance = super().to_representation(instance)

        image_id = instance["image"]
        if not image_id:
            return instance

        image_data = self.instance.image.read()
        instance["image"] = b64encode(image_data).decode("utf-8")

        return instance
