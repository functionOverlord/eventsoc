"""wad_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from eventsoc import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('create_event/', views.create_event, name='Event_add'),
    path('eventsoc/create_event/', views.create_event, name='create_event'),
    path('register/', views.register, name='register'),
    path('edit_event/<slug:slug>/', views.edit_event, name='edit_event'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('booked/', views.booked, name='views'),
    path('account/', views.account, name='account'),
    path('society/', views.society, name='society'),
    path('past_events/', views.past_events, name='past_events'),
    path('user_logout/', views.user_logout, name='user_logout'),
    url(r'^(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
    url(r'^(?P<slug>[\w\-]+)/delete/$',
        views.delete_event, name='delete_event'),
    path('event/<slug:slug>/', views.event, name='event'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
