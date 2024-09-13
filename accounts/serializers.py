from rest_framework import generics, permissions
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True},'email': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],validated_data['password'])

        return user

# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')

# Change Password
from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_code', 'category_description', 'created_on']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_code = serializers.SerializerMethodField()
    # category_code = serializers.CharField(source='category.category_code', read_only=True)

    class Meta:
        model = Product
        fields = ['product_id', 'category','category_code', 'category_id', 'product_name', 'product_details','product_description','actual_price','discounted_price', 'product_image', 'created_by', 'created_on']
    def get_category_code(self, obj):
        return obj.category.category_code
def create(self, validated_data):
        # You can optionally include additional logic here if needed
        return super().create(validated_data)