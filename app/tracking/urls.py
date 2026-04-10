from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path("waiting-dryroom/", views.waiting_dryroom_page, name="waiting_dryroom_page"),
    path("waiting-folding/", views.waiting_folding_page, name="waiting_folding_page"),
    
    path("dryroom/", views.dryroom_transaction_page, name="dryroom_transaction_page"),
    path("folding/", views.folding_transaction_page, name="folding_transaction_page"),
    
    path("api/waiting-dryroom/", api_views.get_garment_waiting_dryroom, name="api_waiting_dryroom"),
    path("api/waiting-folding/", api_views.get_garment_waiting_folding, name="api_waiting_folding"),
    
    path("api/dryroom/checkin/", api_views.dryroom_checkin_api, name="dryroom_checkin_api"),
    path("api/dryroom/checkout/", api_views.dryroom_checkout_api, name="dryroom_checkout_api"),
    
    path("api/folding/checkin/", api_views.folding_checkin_api, name="folding_checkin_api"),
    path("api/folding/checkout/", api_views.folding_checkout_api, name="folding_checkout_api"),
]
