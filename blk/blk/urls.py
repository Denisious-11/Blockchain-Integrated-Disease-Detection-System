"""blk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blk_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),


    ##########login start
    url(r'^$',show_index),
    url(r'^show_index', show_index, name="show_index"),
    url(r'^check_login', check_login, name="check_login"),
    url(r'^logout',logout,name="logout"),
    url(r'^register',register,name="register"),
    ##########login end

    ################Admin start
    url(r'^show_home_admin',show_home_admin,name="show_home_admin"),
    url(r'^show_request_admin',show_request_admin,name="show_request_admin"),
    url(r'^show_users_admin',show_users_admin,name="show_users_admin"),
    url(r'^show_history_admin',show_history_admin,name="show_history_admin"),
    url(r'^approve',approve,name="approve"),
    url(r'^reject',reject,name="reject"),
    url(r'^show_home_patient',show_home_patient,name="show_home_patient"),
    url(r'^temp_del',temp_del,name="temp_del"),
    url(r'^display_test_page',display_test_page,name="display_test_page"),
    url(r'^do_prediction',do_prediction,name="do_prediction"),
]
