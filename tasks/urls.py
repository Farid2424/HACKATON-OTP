"""
URL configuration for tasks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static 
#import host.views
import authentication.views
from django.urls import path



urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('login/', authentication.views.LoginPage.as_view(), name='login'),
    path('logout/', authentication.views.Logout_user.as_view(), name='logout'),
    path('', authentication.views.home, name='home'),
    path('password_change/',authentication.views.PasswordChangeView.as_view(), name = 'password_change'),
    path('password_change/done/', authentication.views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('tache/', authentication.views.tache, name='tache'),
    path('after_tache/<int:tache_id>', authentication.views.after_tache, name='after_tache'),
   #path('Taches/', authentication.views.Taches.as_view(), name='Taches'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
