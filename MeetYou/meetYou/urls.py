from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from accounts import views as accountsViews

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', accountsViews.AccountsView.as_view()),
    path('sign/', accountsViews.SignView.as_view()),
    path('organization/', accountsViews.OrganizationView.as_view()),
    path('admindiv/', accountsViews.AdminDivView.as_view()),
]
