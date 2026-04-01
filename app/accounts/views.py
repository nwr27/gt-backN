from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@api_view(["POST"])
def register_rfid_card(request):
    user_id = request.data.get("user_id")
    username = request.data.get("username")
    rfid_user = str(request.data.get("rfid_user", "")).strip()

    bagian = request.data.get("bagian")
    branch = request.data.get("branch")
    telegram = request.data.get("telegram")
    no_hp = request.data.get("no_hp")

    if not rfid_user:
        return Response(
            {"success": False, "message": "rfid_user wajib diisi"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # cari user dari user_id atau username
    user = None
    if user_id:
        user = User.objects.filter(id=user_id).first()
    elif username:
        user = User.objects.filter(username=username).first()

    if not user:
        return Response(
            {"success": False, "message": "User tidak ditemukan"},
            status=status.HTTP_404_NOT_FOUND
        )

    # cek apakah kartu sudah dipakai user lain
    duplicate = UserProfile.objects.filter(rfid_user=rfid_user).exclude(user=user).first()
    if duplicate:
        return Response(
            {
                "success": False,
                "message": "Kartu RFID sudah terdaftar ke user lain",
                "rfid_user": rfid_user,
                "registered_to": duplicate.user.username
            },
            status=status.HTTP_409_CONFLICT
        )

    with transaction.atomic():
        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.rfid_user = rfid_user

        if bagian is not None:
            profile.bagian = bagian
        if branch is not None:
            profile.branch = branch
        if telegram is not None:
            profile.telegram = telegram
        if no_hp is not None:
            profile.no_hp = no_hp

        profile.save()

    return Response(
        {
            "success": True,
            "message": "Kartu RFID berhasil didaftarkan",
            "data": {
                "user_id": user.id,
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "rfid_user": profile.rfid_user,
                "bagian": profile.bagian,
                "branch": profile.branch,
                "telegram": profile.telegram,
                "no_hp": profile.no_hp,
            }
        },
        status=status.HTTP_200_OK
    )
    
@api_view(["POST"])
def create_user_with_rfid(request):
    username = str(request.data.get("username", "")).strip()
    password = str(request.data.get("password", "")).strip()
    first_name = str(request.data.get("first_name", "")).strip()
    last_name = str(request.data.get("last_name", "")).strip()
    email = str(request.data.get("email", "")).strip()
    rfid_user = str(request.data.get("rfid_user", "")).strip()

    bagian = request.data.get("bagian")
    branch = request.data.get("branch")
    telegram = request.data.get("telegram")
    no_hp = request.data.get("no_hp")

    if not username or not password or not rfid_user:
        return Response(
            {
                "success": False,
                "message": "username, password, dan rfid_user wajib diisi"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"success": False, "message": "Username sudah dipakai"},
            status=status.HTTP_409_CONFLICT
        )

    if UserProfile.objects.filter(rfid_user=rfid_user).exists():
        return Response(
            {"success": False, "message": "Kartu RFID sudah terdaftar"},
            status=status.HTTP_409_CONFLICT
        )

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.rfid_user = rfid_user
        if bagian is not None:
            profile.bagian = bagian
        if branch is not None:
            profile.branch = branch
        if telegram is not None:
            profile.telegram = telegram
        if no_hp is not None:
            profile.no_hp = no_hp

        profile.save()

    return Response(
        {
            "success": True,
            "message": "User dan kartu RFID berhasil dibuat",
            "data": {
                "user_id": user.id,
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "rfid_user": profile.rfid_user,
                "bagian": profile.bagian,
                "branch": profile.branch,
                "telegram": profile.telegram,
                "no_hp": profile.no_hp,
            }
        },
        status=status.HTTP_201_CREATED
    )
@login_required
def rfid_registration_page(request):
    return render(request, 'rfid_registration.html')