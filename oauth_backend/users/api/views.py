from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView

from oauth_backend.users.models import User

from .serializers import UserSerializer


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "home"
    client_class = OAuth2Client
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except OAuth2Error as e:
            print(str(e))
            if "Request to user info failed" in str(e):
                raise AuthenticationFailed("Google token expired")
            else:
                raise AuthenticationFailed("Failed to authenticate with Google")


class AuthToken(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        # assert isinstance(self.request.user.id, int)
        serializer = UserSerializer(instance=request.user, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)



class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
