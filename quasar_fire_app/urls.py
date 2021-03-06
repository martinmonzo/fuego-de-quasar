from django.urls import path

from quasar_fire_app.views.top_secret import TopSecretAPIView


urlpatterns = [
    path('topsecret/', TopSecretAPIView.as_view()),
]