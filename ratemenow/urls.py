from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.authtoken import views as authtokenview

from place import views
from place import views_api

router = routers.DefaultRouter()
router.register(r"place", views_api.PlaceViewSet)
router.register(r"user", views_api.CreateUserViewSet)

urlpatterns = [
    # Kelompok URL Authentification Website
    url(r'^$', views.homepage, name='homepage'),
    url(r'^auth/login', views.loginpage , name='loginpage'),
    url(r'^auth/logout', views.logoutpage , name='logoutpage'),
    url(r'^auth/reg', views.regpage , name='regpage'),

    url(r'^admin/', admin.site.urls),

    # Kelompok URL Webapps
    url(r'^addplace/$', views.add_place, name='addplace'),
    url(r'^place/(?P<place_id>\d+)/edit$', views.edit_place, name='editplace'),
    url(r'^place/(?P<place_id>\d+)/delete$', views.delete_place, name='deleteplace'),
    url(r'^place/(?P<place_id>\d+)/detail$', views.detail_place, name='detailplace'),

    # Kelompok URL API
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-auth-token/', authtokenview.obtain_auth_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
