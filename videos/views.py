from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Video
from users.models import UserProfile
from hashids import Hashids
from .models import Video




def video_list(request):
    # Retrieve all videos
    videos = Video.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})


@login_required  # This will ensure the user is logged in before uploading
def video_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES.get('video_file')
        
        if not title or not video_file:
            return JsonResponse({'error': 'Missing title or video file'}, status=400)

        # Get the logged-in user's profile
        user_profile = request.user.profile  # Access the UserProfile related to the user

        # Create and save the video
        video = Video.objects.create(
            title=title,
            video_file=video_file,
            user=user_profile  # Assign the correct user profile
        )

        # Generate the unique video link
        video_link = video.generate_link()

        return JsonResponse({'message': 'Video uploaded successfully!', 'link': video_link}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)