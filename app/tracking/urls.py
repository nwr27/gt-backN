from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path("waiting-dryroom/", views.waiting_dryroom_page, name="waiting_dryroom_page"),
    path("filter-garment/", views.filter_garment_page, name="filter_garment_page"),
    path("api/waiting-dryroom/", api_views.get_garment_waiting_dryroom, name="api_waiting_dryroom"),
]
