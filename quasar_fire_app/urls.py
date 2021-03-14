from django.conf.urls import url
from django.urls import path

from quasar_fire_app.views.top_secret import TopSecretAPIView
from quasar_fire_app.views.top_secret_split_get import TopSecretSplitGetAPIView
from quasar_fire_app.views.top_secret_split_post import TopSecretSplitPostAPIView


urlpatterns = [
    path('topsecret/', TopSecretAPIView.as_view()),
    path('topsecret_split/', TopSecretSplitGetAPIView.as_view()),
    url(r'^topsecret_split/(?P<satellite_name>\w+)/$', TopSecretSplitPostAPIView.as_view()),
]