from django.urls import path

from oauth_backend.users.api.views import GoogleLoginView, AuthToken

app_name = 'users.api'

urlpatterns = [
    path("api/login/google/", GoogleLoginView.as_view(), name="google_login"),
    path("api/authentication-oauth/", AuthToken.as_view(), name="authentication-suaviagem")
]