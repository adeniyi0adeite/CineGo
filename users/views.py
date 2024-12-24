from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        # Debugging: Print the username to ensure it's being captured
        print(f"Username: {username}")

        # Check if the username is empty
        if not username:
            return JsonResponse({'error': "Username must not be empty"}, status=400)

        # Validation checks
        if password != confirm_password:
            return JsonResponse({'error': "Passwords don't match"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': "Username already exists"}, status=400)

        # Create new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Log the user in
        auth_login(request, user)
        
        # Return success response with redirect URL
        return JsonResponse({'success': 'Welcome, you are now registered!', 'redirect': '/'}, status=200)
    
    # Render the registration template for GET request
    return render(request, 'users/register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': 'You have successfully logged in!', 'redirect': '/'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=400)

    # Render the login template for GET request
    return render(request, 'users/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logging out
