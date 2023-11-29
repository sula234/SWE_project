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
    # driver_name = serializers.SerializerMethodField()
    # vehicle_plate_number = serializers.SerializerMethodField()

    class Meta:
        model = FuelReport
        fields = '__all__'

    # def get_driver_name(self, obj):
    #     # Compute the value for additional_field1
    #     # For example, return a combination of other fields or a computed value
    #     return self.fuel_reports
    #
    # def get_vehicle_plate_number(self, obj):
    #     # Compute the value for additional_field2
    #     # This could be any logic that makes sense for your application
    #     return "Computed Value 2"