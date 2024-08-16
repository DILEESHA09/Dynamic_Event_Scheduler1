import datetime
from rest_framework import serializers
from .models import Events,Sessions

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'title', 'description', 'date', 'location']

    def validate_date(self, value):
        # Custom validation example: ensure date is not in the past
        if value < datetime.date.today():
            raise serializers.ValidationError("The event date cannot be in the past.")
        return value

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = ['id', 'event_id', 'title', 'start_time', 'end_time', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Check that end_time is after start_time.
        """
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data
