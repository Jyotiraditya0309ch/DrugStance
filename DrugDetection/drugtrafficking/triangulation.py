from .models import UserProfile, Post

class Triangulation:
    def triangulate(self, user_id):
        """Triangulate key identifiers for a given user."""
        user_profile = UserProfile.objects.get(id=user_id)
        
        # Fetch posts related to this user
        posts = Post.objects.filter(user=user_profile)

        identifiers = {
            "user_id": user_profile.id,
            "email": user_profile.email,
            "mobile": user_profile.mobile_number,
            "ip_addresses": [],
            "posts": []
        }

        # Assuming you have a way to retrieve IP addresses from posts
        for post in posts:
            identifiers["ip_addresses"].append(post.ip_address)
            identifiers["posts"].append({
                "content": post.content,
                "timestamp": post.created_at
            })

        return identifiers
