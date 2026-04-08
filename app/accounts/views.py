from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GarmentRegistrationForm

from .models import UserProfile

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def garment_rfid_registration(request):
    if request.method == "POST":
        form = GarmentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Garment card registered successfully.")
            return redirect("garment_rfid_registration")
    else:
        form = GarmentRegistrationForm()

    return render(request, "accounts/garment_rfid_registration.html", {"form": form})
    
@login_required
def rfid_registration_page(request):
    return render(request, 'accounts/rfid_registration.html')