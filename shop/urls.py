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
from django.contrib import admin
from django.urls import path, include

from apps.utils.image_uploader import upload
from apps.utils.verification_code import verification_code

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/upload', upload),
    path('api/verification_code', verification_code),

    path('api/account/', include(('apps.account.urls', 'apps.account'), namespace='account')),
    path('api/course/', include(('apps.course.urls', 'apps.course'), namespace='course')),
    path('api/cart/', include(('apps.cart.urls', 'apps.cart'), namespace='cart')),
]
