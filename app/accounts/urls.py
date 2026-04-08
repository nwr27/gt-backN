from django.urls import path
from .views import rfid_registration_page, garment_rfid_registration

urlpatterns = [
    path("users/rfid/register/", rfid_registration_page, name="user_rfid_register"),
    path("garments/rfid/register/", garment_rfid_registration, name="garment_rfid_register"),
]
