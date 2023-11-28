from rest_framework import serializers

from users.models import Driver, User, Route, FuelPreson, FuelReport


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FuelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelPreson
        fields = '__all__'


class FuelingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelReport
        fields = '__all__'
