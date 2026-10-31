"""
URL configuration for society project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from client import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('register/',views.register),
    path('', views.index, name='home'),
    path('complaints/',views.table),
    path('member_list/',views.member_list),
    path('notice/',views.notices),
    path('events/',views.event),
    path('house_worker/',views.houseworker),
    path('house_worker/<str:name>',views.houseworker),
    path('house_worker_type/',views.houseworkertype),
    path('forms/',views.add_complain),
    path('profile/',views.profile),
    path('family_member/',views.family_member),
    path('delete_family/<int:id>',views.delete_family),
    path('add_family/',views.add_family),
    path('index/',views.index),
    path('logout/',views.logout),
    path('clubhousebooking/',views.clubhouse),
    path('booking_form/',views.clubhousebooking),
    path('forgot_password/',views.forgot_pwd),
    path('send_otp/',views.sendotp),
    path('set_pwd/',views.set_password),
    path('reciept/',views.rec),
    path('maintanance_payment/',views.maintanance_pay),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)