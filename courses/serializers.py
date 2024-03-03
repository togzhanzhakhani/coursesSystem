from rest_framework import serializers
from .models import Product, Lesson, Group, Purchase

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['user', 'product']

class ProductStatisticsSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    students_count = serializers.IntegerField()
    groups_count = serializers.IntegerField()
    average_fill_percentage = serializers.FloatField()
    access_percentage = serializers.FloatField()
