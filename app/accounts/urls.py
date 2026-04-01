from django.urls import path
from .views import (register_rfid_card, 
                    create_user_with_rfid,
                    rfid_registration_page
                    )

urlpatterns = [
    path("register-rfid/", register_rfid_card, name="register_rfid_card"),
    path("create-user-rfid/", create_user_with_rfid, name="create_user_with_rfid"),
    path("rfid-registration-page/", rfid_registration_page, name="rfid_registration_page"),
]