from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path("waiting-dryroom/", views.waiting_dryroom_page, name="waiting_dryroom_page"),
    path("api/waiting-dryroom/", api_views.get_garment_waiting_dryroom, name="api_waiting_dryroom"),
    
    path("waiting-folding/", views.waiting_folding_page, name="waiting_folding_page"),
    path("api/waiting-folding/", api_views.get_garment_waiting_folding, name="api_waiting_folding"),
]
