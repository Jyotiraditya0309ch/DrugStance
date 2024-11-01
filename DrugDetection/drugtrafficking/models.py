from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """Model representing a post made by users on the social media platform."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()  # Text content of the post
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Optional image
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)  # Optional video
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when post was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when post was last updated
    flagged = models.BooleanField(default=False)  # Indicates if the post is flagged for review

    def __str__(self):
        return f'Post by {self.user.username} at {self.created_at}'

class UserProfile(models.Model):
    """Model representing additional information about users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # User's IP address
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  # User's mobile number
    email = models.EmailField(blank=True, null=True)  # User's email address
    flagged_posts = models.ManyToManyField(Post, blank=True, related_name='flagged_by')  # Posts flagged by the user

    def __str__(self):
        return f'Profile of {self.user.username}'

class FlaggedContent(models.Model):
    """Model representing flagged content for further analysis."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Reference to the flagged post
    reason = models.TextField()  # Reason for flagging the content
    flagged_at = models.DateTimeField(auto_now_add=True)  # Timestamp when content was flagged
    resolved = models.BooleanField(default=False)  # Indicates if the flagged content has been reviewed

    def __str__(self):
        return f'Flagged Content: {self.post} - Reason: {self.reason}'

class TraffickerProfile(models.Model):
    """Model representing profiles of suspected traffickers."""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    suspicious_activity_count = models.IntegerField(default=0)  # Count of suspicious activities
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the profile was created

    def __str__(self):
        return f'Trafficker Profile: {self.user_profile.user.username} - Count: {self.suspicious_activity_count}'
