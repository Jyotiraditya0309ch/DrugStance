from .models import UserProfile, FlaggedContent

class Profiling:
    def build_profile(self, user_id):
        """Build a profile for a user based on their flagged activities."""
        user_profile = UserProfile.objects.get(id=user_id)
        flagged_posts = FlaggedContent.objects.filter(post__user=user_profile)

        profile_data = {
            "user_id": user_profile.id,
            "username": user_profile.username,
            "flagged_count": flagged_posts.count(),
            "flagged_posts": []
        }

        for flagged in flagged_posts:
            profile_data["flagged_posts"].append({
                "post_content": flagged.post.content,
                "reason": flagged.reason,
                "timestamp": flagged.created_at
            })

        return profile_data
