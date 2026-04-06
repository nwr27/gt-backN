from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from accounts.views import dashboard
from django.urls import include

def root_redirect(request):
    return redirect('/login/')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
]