from rest_framework import serializers
from .models import users, jobpost, company

class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'

class jobpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = jobpost
        fields = '__all__'

class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'

