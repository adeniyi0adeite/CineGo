
# videos/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from .models import Video, VideoAccess
import os


@login_required
def video_list(request):
    videos = Video.objects.all()
    user_profile = request.user.userprofile

    # Call the method to check for active subscription
    active_subscription = user_profile.get_active_subscription()

    # Determine if the user has an active subscription
    has_active_subscription = active_subscription is not None

    # Get pay-per-watch access (VideoAccess objects for the user)
    pay_per_watch_access_videos = VideoAccess.objects.filter(user=user_profile).values_list('video_id', flat=True)

    # Debugging output
    print("All videos:", videos)
    print("Pay-per-watch access videos:", pay_per_watch_access_videos)

    return render(request, 'videos/video_list.html', {
        'all_videos': videos,
        'pay_per_watch_videos': pay_per_watch_access_videos,  # List of video IDs the user has pay-per-watch access to
        'has_active_subscription': has_active_subscription,
    })




ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/mkv', 'video/webm']


@login_required
@csrf_exempt
def video_upload(request):
    if request.method == 'GET':
        # Render the video upload form
        return render(request, 'videos/video_upload.html')

    if request.method == 'POST':
        try:
            # Fetch title, video file, and price from the POST request
            title = request.POST.get('title')
            video_file = request.FILES.get('video_file')
            price = request.POST.get('price')

            # Check if title, video file, or price is missing
            if not title or not video_file or not price:
                raise ValidationError('Please provide a title, a video file, and a price.')

            # Convert price to a Decimal
            price = float(price)  # Ensure the price is a float

            # Validate the video file type
            if video_file.content_type not in ALLOWED_VIDEO_TYPES:
                raise ValidationError('Invalid file type. Please upload MP4, MKV, or WEBM videos.')

            # Check if the file exceeds the size limit
            max_upload_size = settings.DATA_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)  # Convert to MB
            if video_file.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
                raise ValidationError(f'File too large. Maximum allowed size is {max_upload_size} MB.')

            # Fetch user profile
            user_profile = request.user.userprofile

            # Check if the video with the same title already exists for the user
            existing_video = Video.objects.filter(title=title, user=user_profile).first()

            if existing_video:
                return JsonResponse({'error': 'A video with this title already exists.'}, status=400)

            # Create and save the video instance with price
            video = Video.objects.create(
                title=title,
                video_file=video_file,
                price=price,  # Assign the price here
                user=user_profile
            )

            # Generate a unique link for the video
            video_link = video.generate_link()

            # Return a success response as JSON
            return JsonResponse({'message': 'Video uploaded successfully!', 'video_link': video_link}, status=200)

        except ValidationError as ve:
            # Handle validation errors
            return JsonResponse({'error': str(ve)}, status=400)

        except Exception as e:
            # Catch any unexpected exceptions
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@login_required
def video_stream(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user_profile = request.user.userprofile

    # Check for active subscription
    active_subscription = user_profile.get_active_subscription()
    has_active_subscription = active_subscription is not None

    # Check if the user has pay-per-watch access to this video
    video_access = VideoAccess.objects.filter(user=user_profile, video=video).exists()

    # Default free watch time limit (in seconds)
    free_watch_time = video.free_watch_time.total_seconds()

    # If the user has an active subscription or pay-per-watch access, set free watch time to 0 (unlimited access)
    if has_active_subscription or video_access:
        free_watch_time = 0

    # Determine if the pay button should be shown
    show_pay_button = not (has_active_subscription or video_access)

    return render(request, 'videos/video_stream.html', {
        'video': video,
        'free_watch_time': free_watch_time,  # Pass this as a number (seconds)
        'show_pay_button': show_pay_button,  # Flag to show/hide the pay button
    })
