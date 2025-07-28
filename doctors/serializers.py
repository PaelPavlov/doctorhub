from rest_framework import serializers
from .models import DoctorProfile, WorkingHour

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = ['day', 'start_time', 'end_time']

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    working_hours = WorkingHourSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialty', 'town', 'hospital_name', 'hospital_address', 'telephone', 'working_hours', 'average_rating']

    def get_average_rating(self, obj):
        return round(obj.average_rating(), 1)
