from .models import Post, FlaggedContent, UserProfile

class Analytics:
    def get_overview(self):
        """Get an overview of the current status of posts and users."""
        total_posts = Post.objects.count()
        total_flagged = FlaggedContent.objects.count()
        total_users = UserProfile.objects.count()

        return {
            "total_posts": total_posts,
            "total_flagged": total_flagged,
            "total_users": total_users
        }

    def get_trends(self):
        """Get trends of flagged activities over time."""
        # Example: Group by day and count flagged posts
        trends = FlaggedContent.objects.raw(
            """
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM drugtrafficking_flaggedcontent
            GROUP BY date
            ORDER BY date
            """
        )

        trend_data = [{"date": record.date, "count": record.count} for record in trends]
        return trend_data
