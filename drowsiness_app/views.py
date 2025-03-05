import datetime
import os
from django.http import JsonResponse
import time
import cv2
import imutils
from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance as dist
import numpy as np
import dlib
import pygame.mixer

import asyncio
from asgiref.sync import async_to_sync
from .tasks import drowsiness_detection_task

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser, DriverProfile, Alert, UserSettings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponse

# Global variable to store the running task
running_task = None


def home(request):
    context = {
        "app_name": "DrowsiSense",
        "year": 2025,
    }
    return render(request, "index.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('driver_dashboard')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('driver_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('driver_dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(username=email, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Registration successful!')
                driver_profile = DriverProfile.objects.create(
                    user=authenticated_user,
                    license_number='KBY 127W',
                    phone_number='0712345678'
                )
                return redirect('driver_dashboard')
            else:
                messages.error(request, 'Authentication failed!')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def driver_view(request):
    user = request.user
    driver_profile = DriverProfile.objects.get(user=user)
    alerts = Alert.objects.filter(driver=driver_profile).order_by("-timestamp")
    user_settings = UserSettings.objects.get_or_create(user=user)[0]
    print("👩",user)
    context = {
        "alerts": alerts,
        "user_settings": user_settings,
    }
    return render(request, "driver_dashboard.html", context)


@login_required
@csrf_protect
def update_settings(request):
    if request.method == "POST":
        user = request.user
        user_settings, created = UserSettings.objects.get_or_create(user=user)

        ear_threshold = request.POST.get("ear_threshold", user_settings.ear_threshold)
        ear_frames = request.POST.get("ear_frames", user_settings.ear_frames)
        yawn_threshold = request.POST.get(
            "yawn_threshold", user_settings.yawn_threshold
        )
        alert_frequency = request.POST.get(
            "alert_frequency", user_settings.alert_frequency
        )

        user_settings.ear_threshold = float(ear_threshold)
        user_settings.ear_frames = int(ear_frames)
        user_settings.yawn_threshold = int(yawn_threshold)
        user_settings.alert_frequency = alert_frequency
        user_settings.save()

        return redirect("driver_dashboard")

    return redirect("driver_dashboard")

@login_required
@csrf_protect
def update_profile(request):
    if request.method == "POST":
        user = request.user
        driver_profile = DriverProfile.objects.get(user=user)

        license_number = request.POST.get("license_number")
        phone_number = request.POST.get("phone_number")

        driver_profile.license_number = license_number
        driver_profile.phone_number = phone_number
        driver_profile.save()

        return redirect("driver_dashboard")

    return redirect("driver_dashboard")

@login_required
@csrf_exempt
def toggle_monitoring(request):
    if request.method == "POST":
        action = request.POST.get("action", "").lower()
        user = request.user

        if action == "start":
            webcam_index = 0  # Default webcam index
            ear_thresh = user.user_settings.ear_threshold
            ear_frames = user.user_settings.ear_frames
            yawn_thresh = user.user_settings.yawn_threshold

             # Retrieve driver_profile and driver_email synchronously
            driver_profile = DriverProfile.objects.get(user=user)
            driver_email = driver_profile.user.email
            
            # Create a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Start the real-time drowsiness detection process asynchronously
                running_task = async_to_sync(drowsiness_detection_task)(
                    webcam_index, ear_thresh, ear_frames, yawn_thresh, driver_profile, driver_email
                )
                request.session['running_task'] = running_task
            finally:
                loop.close()

            return JsonResponse(
                {"action": action, "message": "Monitoring started successfully."}
            )
        elif action == "stop":
            # Stop the drowsiness detection process
            running_task = request.session.get('running_task')
            if running_task is not None:
                async_to_sync(running_task.cancel)()
                del request.session['running_task']
            return JsonResponse(
                {"action": action, "message": "Monitoring stopped successfully."}
            )
    return JsonResponse({"message": "Invalid request method."})


def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect("home")

