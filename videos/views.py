
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
from .models import Video, VideoAccess, Category
from users.models import Actor, Director
from django.core.files.storage import FileSystemStorage



import os
from django.contrib import messages



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



@login_required
def video_categories(request):
    # Fetch all categories
    categories = Category.objects.all()

    # Get videos in each category
    category_videos = {}
    for category in categories:
        category_videos[category] = Video.objects.filter(categories=category)

    return render(request, 'videos/video_categories.html', {
        'category_videos': category_videos,
    })


@login_required
def video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user_profile = request.user.userprofile

    # Check for active subscription
    active_subscription = user_profile.get_active_subscription()
    has_active_subscription = active_subscription is not None

    # Check if the user has pay-per-watch access to this video
    video_access = VideoAccess.objects.filter(user=user_profile, video=video).exists()

    # Default free watch time limit (in seconds)
    free_watch_time = 4  # Set to 4 seconds as default

    # If the user has an active subscription or pay-per-watch access, set free watch time to 0 (unlimited access)
    if has_active_subscription or video_access:
        free_watch_time = 0

    # Determine if the pay button should be shown
    show_pay_button = not (has_active_subscription or video_access)

    # Get the actors and director
    actors = video.actors.all()
    director = video.director

     # Calculate the running time in minutes and cast it to an integer
    running_time_minutes = int(video.running_time.total_seconds() // 60)  # Remove decimal places

    return render(request, 'videos/video.html', {
        'video': video,
        'free_watch_time': free_watch_time,  # Pass this as a number (seconds)
        'show_pay_button': show_pay_button,  # Flag to show/hide the pay button
        'actors': actors,                   # Pass the actors to the template
        'director': director,               # Pass the director to the template
        'running_time_minutes': running_time_minutes,  # Pass the running time in minutes
    })




@login_required
def video_upload(request):
    
    if request.method == "POST":
        # Retrieve form data from request.POST
        title = request.POST.get('title')
        price = request.POST.get('price')
        video_file = request.FILES.get('video_file')

        # Ensure all required fields are filled
        if not title or not price or not video_file:
            messages.error(request, "Please fill in all required fields.")
            return redirect('video_upload')  # URL for the video upload form page

        try:
            # Create a new Video instance and save it
            video = Video(
                title=title,
                price=price,
                video_file=video_file,
                upload_time=timezone.now()
            )

            # Optionally, you can add default or dynamic values for other fields like genre
            video.genre = 'action'  # Example: Set a default genre
            video.parental_guidance = 'PG'  # Example: Set default parental guidance
            video.running_time = timedelta(minutes=90)  # Example: Default running time of 90 minutes
            video.release_date = timezone.now().date()  # Set release date as current date

            # Save the new video
            video.save()

            # Success message
            messages.success(request, "Video uploaded successfully!")
            return redirect('video_list')  # Redirect to the list of videos or another appropriate page

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    # In case of GET or any other method
    return render(request, 'videos/video_upload.html')  # Replace with your form template URL




@login_required
def video_stream(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user_profile = request.user.userprofile

    # Check for active subscription
    active_subscription = user_profile.get_active_subscription()
    has_active_subscription = active_subscription is not None

    # Check if the user has pay-per-watch access to this video
    video_access = VideoAccess.objects.filter(user=user_profile, video=video).exists()

    # Default free watch time limit (in seconds) set to 4 seconds
    free_watch_time = 4  # Set to 4 seconds as default

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
