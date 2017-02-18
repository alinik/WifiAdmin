from django.conf.urls import url
from wifinder.pois.views import data_json

urlpatterns = [
    url(r'data.json$', data_json, name='data.json'),
]
