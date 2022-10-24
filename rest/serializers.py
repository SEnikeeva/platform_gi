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

    class Meta:
        model = OilDeposit
        fields = '__all__'


class WellSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Well
        fields = '__all__'
