from django.shortcuts import render

from videos.models import Video



def custom_page_not_found_view(request, exception):
    return render(request, "cinego/404.html", status=404)

def home_view(request):
    # Get all video objects
    videos = Video.objects.all()
    return render(request, 'cinego/home.html', {'videos': videos})