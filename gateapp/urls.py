from django.contrib import admin
from django.urls import path
from . views import home, user_details_view, success_view, config_nginx

urlpatterns = [
    path('',name='home', view=home),
    path('detail/',name='user_details', view=user_details_view),
    path('success/',name='success', view=success_view),
    path('admin/', admin.site.urls),
    path('configure/', name='config_nginx', view=config_nginx),
]