"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path('create_new_course', views.create_new_course),
    path('get_course_detail', views.get_course_detail),
    path('get_snapshot_detail', views.get_snapshot_detail),
    path('edit_course', views.edit_course),
    path('delete_course', views.delete_course),
    path('publish_course', views.publish_course),
    path('get_latest_courses_list', views.get_latest_courses_list),
    path('get_hottest_courses_list', views.get_hottest_courses_list),
    path('get_pinned_courses_list', views.get_pinned_courses_list),
    path('get_my_courses_list', views.get_my_courses_list),
]
