import re
from django.conf.urls import include
from django.urls import re_path,path
from .views import authentication_test,register_by_access_token

app_name = 'accounts'


accounts_urlpatterns = [
    re_path(r'^api/v1/', include('djoser.urls')),
    re_path(r'^api/v1/', include('djoser.urls.authtoken')),
    re_path('api/v1/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', register_by_access_token),
    path('api/v1/authentication-test/', authentication_test),
]