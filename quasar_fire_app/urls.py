from django.conf.urls import url
from django.urls import path

from quasar_fire_app.views.top_secret import TopSecretAPIView
from quasar_fire_app.views.top_secret_split import TopSecretSplitAPIView


urlpatterns = [
    path('topsecret/', TopSecretAPIView.as_view()),
    url(r'^topsecret_split/(?P<satellite_name>\w+)/$', TopSecretSplitAPIView.as_view()),
]