from .models import FlaggedContent
from django.utils import timezone

class Reporting:
    def generate_report(self):
        """Generate a report of all flagged content."""
        flagged_contents = FlaggedContent.objects.all()

        report_data = {
            "report_date": timezone.now(),
            "total_flagged": flagged_contents.count(),
            "details": []
        }

        for flagged in flagged_contents:
            report_data["details"].append({
                "post_id": flagged.post.id,
                "user": flagged.post.user.username,
                "reason": flagged.reason,
                "timestamp": flagged.created_at
            })

        return report_data

    def send_alert(self, flagged_content):
        """Send alert for a flagged content."""
        # Here you can implement logic to send an alert (e.g., email, push notification)
        print(f"Alert: Post by {flagged_content.post.user.username} flagged for {flagged_content.reason}.")
