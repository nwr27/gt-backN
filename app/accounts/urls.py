from django.urls import path
from .views import (rfid_registration_page,
                    garment_rfid_registration
                    )

urlpatterns = [
    path("user/rfid/registration/", rfid_registration_page, name="rfid_registration_page"),
    path("garment/rfid/registration/", garment_rfid_registration, name="garment_rfid_registration"),
]