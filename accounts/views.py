
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from social_django.utils import psa

from requests.exceptions import HTTPError
import urllib
import json

@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def register_by_access_token(request, backend):
    token = request.data.get('access_token')
    user = request.backend.do_auth(token)
    print(request)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key
            },
            status=status.HTTP_200_OK,
            )
    else:
        return Response(
            {
                'errors': {
                    'token': 'Invalid token'
                    }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET', 'POST'])
def authentication_test(request):
    print(request.user)
    return Response(
        {
            'message': "User successfully authenticated"
        },
        status=status.HTTP_200_OK,
    )

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def update_user_social_data(request, *args, **kwargs):
    user = kwargs['user']
    if not kwargs['is_new']:
        return
    user = kwargs['user']
    if kwargs['backend'].__class__.__name__ == 'FacebookBackend':
        fbuid = kwargs['response']['id']
        access_token = kwargs['response']['access_token']

        url = 'https://graph.facebook.com/{0}/' \
            '?fields=email,gender,name' \
            '&access_token={1}'.format(fbuid, access_token,)

        photo_url = "http://graph.facebook.com/%s/picture?type=large" \
            % kwargs['response']['id']
        request = urllib.Request(url)
        response = urllib.urlopen(request).read()
        email = json.loads(response).get('email')
        name = json.loads(response).get('name')
        gender = json.loads(response).get('gender')
        return email
