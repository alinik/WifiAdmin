import json

import sequences
from collections import defaultdict

from django.db.models import Count
from django.http import HttpResponse
from django.http import JsonResponse
from sequences import get_next_value
from sequences.models import Sequence

from wifinder.pois.models import Poi, AvailableField, DisplayRole
CAPITAL={
    'Iran':[35.69439,51.42151],
    'Iraq':[33.34058,44.40088]
}

def data_json(request):
    return JsonResponse(data(request))


def data(request):
    pois = Poi.objects.all()
    province_flat = Poi.objects.values('city__region__name', 'status__name', 'city__latitude',
                                       'city__longitude').annotate(c=Count('city__region__name'))
    province = defaultdict(dict)
    for item in province_flat:
        if 'Total' not in province[item['city__region__name']]:
            province[item['city__region__name']]['Total'] = 0
        province[item['city__region__name']]['Total'] += item['c']
        province[item['city__region__name']][item['status__name']] = item['c']
        if 'coord' not in province[item['city__region__name']]:
            province[item['city__region__name']]['coord'] = [float(item['city__latitude']),
                                                             float(item['city__longitude'])]
    for item in province:
        info = '<br/>'.join(['%s:%s' % (x, y) for (x, y) in province[item].items() if x not in ['name', 'coord']])
        province[item]['info'] = '<div dir="rtl">' + info+'</div>'

    province_list = [dict({'name': key}, **province[key]) for key in province]
    country_flat = Poi.objects.values('city__country__name', 'status__name', 'city__latitude',
                                      'city__longitude').annotate(c=Count('city__country__name'))
    country = defaultdict(dict)
    for item in country_flat:
        if 'Total' not in country[item['city__country__name']]:
            country[item['city__country__name']]['Total'] = 0
        country[item['city__country__name']]['Total'] += item['c']
        country[item['city__country__name']][item['status__name']] = item['c']
        if 'coord' not in country[item['city__country__name']]:
            country[item['city__country__name']]['coord'] = CAPITAL[item['city__country__name']]
            # country[item['city__country__name']]['coord'] = [float(item['city__latitude']),
            #                                                  float(item['city__longitude'])]
    for item in country:
        info = '<br/>'.join(['%s:%s' % (x, y) for (x, y) in country[item].items() if x not in ['name', 'coord']])
        country[item]['info'] = '<div dir="rtl">' + info+'</div>'

    country_list = [dict({'name': key}, **country[key]) for key in country]
    result = {
        "detail": [],
        "province": province_list,
        "country": country_list,
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
    user = request.user or 'guest'
    fields = DisplayRole.objects.first().fields.all()
    for poi in pois:
        info = ''

        for field in fields:
            info += '<p>%s:%s</p>' % (field.title or field.name, str(poi.__getattribute__(field.name) or '-'))

        item = {'name': poi.name,
                'status': poi.status.name,
                'province': poi.region.name,
                'country': poi.country.name,
                'coord': [float(poi.location.latitude), float(poi.location.longitude)],
                '3G': poi.mci,
                'info': info
                }
        result['detail'].append(item)

    return result


def get_version(request):
    version = Sequence.objects.get(name='version').last
    return JsonResponse({"version": version, "path": "/js/data.json"})
