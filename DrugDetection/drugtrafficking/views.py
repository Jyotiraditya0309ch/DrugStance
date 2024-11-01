from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import Post, UserProfile, FlaggedContent
from .serializers import PostSerializer, UserProfileSerializer, FlaggedContentSerializer
from .blacklist_post import get_blacklisted_post
#from .detection_model import detect_content  # Import your content detection function
from django.http import JsonResponse
import json
from .drug_customer_dealer_info import get_drug_dealer_customer_data

from .scan_social_media import pt
 # Import the function from scan.py
from django.http import JsonResponse
#from .scan import fetch_suspected_users_with_location 

# api/drugtrafficking/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response



def index(request):
    return render(request,'index.html')

class PostListView(generics.ListCreateAPIView):
    """View to list all posts and create a new post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Override create method to handle additional logic if needed."""
        return super().create(request, *args, **kwargs)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a specific post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class UserProfileView(generics.RetrieveUpdateAPIView):
    """View to retrieve or update a user's profile."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Override to get the profile of the authenticated user."""
        return self.get_queryset().get(user=self.request.user)

class DetectContentView(generics.CreateAPIView):
    #View to detect content in a post
    queryset = Post.objects.all()
    serializer_class = PostSerializer  # Reuse for input, may change based on requirements
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_data = request.data

        # Call your content detection function
        result = detect_content(post_data)  # Implement your logic in the detection model

        return Response(result, status=status.HTTP_200_OK)

class FlaggedPostsView(generics.ListAPIView):
    """View to list all flagged posts."""
    queryset = FlaggedContent.objects.all()
    serializer_class = FlaggedContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Override to filter flagged posts."""
        return super().get_queryset().filter(post__flagged=True)

class FlagPostView(generics.CreateAPIView):
    """View to flag a post."""
    queryset = FlaggedContent.objects.all()
    serializer_class = FlaggedContentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Override create method to flag a post."""
        post_id = request.data.get('post_id')
        reason = request.data.get('reason')

        try:
            post = Post.objects.get(id=post_id)
            flagged_content = FlaggedContent.objects.create(post=post, reason=reason)
            return Response({"message": "Post flagged successfully."}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class AnalyticsView(generics.GenericAPIView):
    """View for analytics and reporting."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Override get method to provide analytics data."""
        # Implement analytics logic here
        analytics_data = {
            "total_posts": Post.objects.count(),
            "flagged_posts": FlaggedContent.objects.count(),
            "user_profiles": UserProfile.objects.count(),
        }
        return Response(analytics_data, status=status.HTTP_200_OK)




@api_view(['GET'])
def analytics_view(request):
    # Sample data for testing purposes
    analytics_data = {
        "trafficData": [
            {"label": "January", "value": 10, "trendValue": 5},
            {"label": "February", "value": 15, "trendValue": 10},
            {"label": "March", "value": 20, "trendValue": 15},
        ],
        "userActivity": [
            {"user": "User1", "activityCount": 5},
            {"user": "User2", "activityCount": 3},
            {"user": "User3", "activityCount": 8},
        ]
    }
    return Response(analytics_data)



@api_view(['GET'])
def scan_all_content(request):
    print("YE")
    try:
        print("YEE")

        scan_results=get_blacklisted_post()
        
        print(scan_results)
        
        return JsonResponse(scan_results,safe=False)

    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# views.py
 # Ensure this function includes location data

def analytics_data(request):
    data={"a":"B"}
    # data = fetch_suspected_users_with_location()  # Returns JSON with user ID, activity, and location
    return JsonResponse(data, safe=False)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import UserProfile  # Assume you have a UserProfile model

def get_user_profile(request):
    if request.method == 'GET':
        # Optionally, you could check if the user is authenticated
        # if not request.user.is_authenticated:
        #     return JsonResponse({'error': 'Unauthorized'}, status=401)

        # Fetch user profile from the database
        #user_profile = get_object_or_404(UserProfile, id=user_id)

        #Alternatively, if you want to use dummy data:
        user_profile = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'age': 30,
            'location': 'New York, USA',
        }

        data = {
            'name': user_profile["name"],
            'email': user_profile["email"],
            'age': user_profile["age"],
            'location': user_profile["location"],
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)



from django.http import JsonResponse
import json
from .suspected_user_info import get_suspect_data  # Adjust import based on where `get_suspect_data` is defined

def get_user_info(request, userId):
    suspected_user_data = get_suspect_data()
    user_info = next((user for user in suspected_user_data if user['id'] == userId), None)
    
    if user_info:
        return JsonResponse(user_info)
    else:
        return JsonResponse({"error": "User not found"}, status=404)

def get_all_users(request):
    suspected_user_data = get_suspect_data()
    if suspected_user_data:
        return JsonResponse(suspected_user_data,safe=False)
    else:
        return JsonResponse({"error": "User not found"}, status=404)

@api_view(['GET'])
def get_comments(request):
    data=get_drug_dealer_customer_data()
    if data:
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({"error": "User not found"}, status=404)

    





