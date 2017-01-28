from django.conf.urls import url
from wifinder.pois.views import data_js, data_json

urlpatterns = [
    url(r'data.js$', data_js, name='data.js'),
    url(r'data.json$', data_json, name='data.json'),
]
