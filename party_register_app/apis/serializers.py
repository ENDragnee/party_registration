# registration/apis/serializers.py
from rest_framework import serializers
from party_register_app.models import Guest


class GuestSerializer(serializers.ModelSerializer):
    # We can expose the human-readable version of the choice field
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Guest
        # Fields to include in the API response
        fields = [
            'unique_id',
            'name',
            'phone_number',
            'will_attend',
            'status',
            'status_display',
            'created_at',
        ]
        # These fields are set by the system, not by the API user directly
        read_only_fields = ['unique_id', 'status', 'created_at']

    def validate_will_attend(self, value):
        """
        Ensure that guests created via API must consent to attend.
        """
        if not value:
            raise serializers.ValidationError("Guests must agree to attend to be registered via the API.")
        return value
