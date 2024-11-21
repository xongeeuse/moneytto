from rest_framework import serializers
from .models import Category, Post, PostLike, Comment
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'category', 'expenses_date', 'content', 'image', 'price', 'privacy_setting', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("가격은 음수일 수 없습니다.")
        return value


class PostLikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    uesr = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'expenses_date', 'content', 'created_at', 'updated_at']


class CalendarMainSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'expenses_date', 'image']

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None
    

class PostDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='category.category_name')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'expenses_date', 'image', 'content', 'category_name', 'created_at', 'updated_at']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')

            return request.build_absolute_uri(obj.image.url)
        return None