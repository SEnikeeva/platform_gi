from rest_framework import serializers

from rest.models import *


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    oil_deposits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class OilDepositSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    wells = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    coords = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    perforations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = OilDeposit
        fields = '__all__'


class WellSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    coords = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    perforations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Well
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Coords
        fields = '__all__'


class PerforationSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Perforation
        fields = '__all__'
