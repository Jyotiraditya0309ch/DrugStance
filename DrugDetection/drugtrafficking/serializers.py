from rest_framework import serializers
from .models import Post, UserProfile, FlaggedContent

class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'video', 'created_at', 'updated_at', 'flagged']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model."""
    
    class Meta:
        model = UserProfile
        fields = ['user', 'ip_address', 'mobile_number', 'email', 'flagged_posts']
        read_only_fields = ['user', 'flagged_posts']

class FlaggedContentSerializer(serializers.ModelSerializer):
    """Serializer for the FlaggedContent model."""
    
    class Meta:
        model = FlaggedContent
        fields = ['id', 'post', 'reason', 'flagged_at', 'resolved']
        read_only_fields = ['id', 'flagged_at', 'resolved']
