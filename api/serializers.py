from rest_framework import serializers
from .models import KBEntry

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    company_name = serializers.CharField(max_length=255)

class KBEntrySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    class Meta:
        model = KBEntry
        fields = ['id', 'question', 'answer', 'category']
