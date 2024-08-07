# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.http import JsonResponse
from urllib.parse import unquote

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        data = None
        token_id = None
        if token_id:
            data = self._decode_id_token(app, token_id)
            if self.fetch_userinfo and "picture" not in data:
                data.update(self.get_user_info(token))
                picture = data.get("picture")
                if picture:
                    data["picture"] = picture
        else:
            data= self._decode_id_token(app, token.token)

        return self.get_provider().sociallogin_from_response(request, data)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000"
    client_class = OAuth2Client

def decode_code_view(request):
    code = request.GET.get('code', None)
    if code:
        decoded_code = unquote(code)
        return JsonResponse({'decoded_code': decoded_code})
    return JsonResponse({'error': 'No code parameter found'}, status=400)


class TestAccessTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })