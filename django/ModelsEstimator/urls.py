from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from ModelsEstimator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect),
    path('auth/', views.auth),
    path('logout/', views.logout),
    path('panel/', include("Panel.urls")),
]
