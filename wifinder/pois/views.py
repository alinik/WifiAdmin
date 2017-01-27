import json

from django.http import HttpResponse
from django.http import JsonResponse

from wifinder.pois.models import Poi


def data_json(request):
    return JsonResponse(data())


def data_js(request):
    valid_json = json.dumps(data())
    return HttpResponse('document.markers=' + valid_json, content_type='text/javascript')


def data():
    pois = Poi.objects.all()
    result = {"detail": [],
              "province": [],
              "country": []
              }

    """
            "info": "<div class=\"green\"><h2>\u0641\u0631\u0648\u062f\u06af\u0627\u0647 \u0645\u0647\u0631\u0622\u0628\u0627\u062f \u062a\u0631\u0645\u06cc\u0646\u0627\u0644 6</h2><p>\u0641\u0631\u0648\u062f\u06af\u0627\u0647 \u0645\u0647\u0631\u0627\u0628\u0627\u062f- \u062a\u0631\u0645\u06cc\u0646\u0627\u0644 6</p><p>3G:</p></div>",
        "status": "On - Air",
        "province": "\u062a\u0647\u0631\u0627\u0646",
        "name": "\u0641\u0631\u0648\u062f\u06af\u0627\u0647 \u0645\u0647\u0631\u0622\u0628\u0627\u062f \u062a\u0631\u0645\u06cc\u0646\u0627\u0644 6",
        "country": "Iran",
        "coord": [
            35.688786,
            51.330155
        ],
        "3G": []
    """
    # user = request
    for poi in pois:
        item = {'name': poi.name,
                'status': poi.status.name_persian,
                'province': poi.region.name,
                'country': poi.country.name,
                'coord': [float(poi.location.latitude),float(poi.location.longitude)],
                '3G':poi.mci,
                'info':''
                }
        result['detail'].append(item)
    return result
