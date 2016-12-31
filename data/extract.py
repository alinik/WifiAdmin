#!/usr/bin/env python
# coding=utf-8
import csv
import json
import os

DEBUG = os.environ.get('DEBUG', False)

color = {
    'Nominal': "gray",  # gray
    'S.A Done': "yellow",  # yellow
    'A.P.Installation.Done': "purple",  # purple
    'B.H.Installation.Done': "blue",  # blue
    'On - Air': "green",  # green
    'Switched Off': "white"  # white
}

STATUES = [
    'Nominal',
    'S.A Done',
    'A.P.Installation.Done',
    'B.H.Installation.Done',
    'On - Air',
    'Switched Off',
]
RESULT_FILE = 'src/js/data.js'
f = open('data/data.csv')

t = csv.reader(f)
good = bad = 0
result = []

for c, i in enumerate(t):
    try:
        lat_str = i[11]
        lon_str = i[12]
        if ord(lat_str[-1]) == 176:
            lat_str = lat_str[:-2]
        if ord(lon_str[-1]) == 176:
            lon_str = lon_str[:-2]
        lat = float(lat_str)
        lon = float(lon_str)
        access_3g = [i[16] == 'دارد', i[17] == 'دارد', i[18] == 'دارد']
        result.append({
            'name': i[4],
            'coord': [lat, lon],
            'info': '<div class="{}"><h2>{}</h2><p>{}</p>'
                    '<p>3G:{}</p></div>'.format(color.get(i[27], 'gray'), i[4], i[13], '،'.join(
                [t for x, t in enumerate(['ایرانسل', 'رایتل', 'همراه اول']) if access_3g[x]])),
            'status': i[27],
            'province': i[2],
            '3G': [t for x, t in enumerate(['ایرانسل', 'رایتل', 'همراه اول']) if access_3g[x]],
            'country': i[28]
        })
        # print c,i[0],'ok'
        good += 1
    except Exception as e:
        print(c, i[0], 'bad coord: {},{}'.format(i[1], i[2]))
        bad += 1

# Aggregation
province_agg = {}
for item in result:
    if item['province'] not in province_agg:
        province_agg[item['province']] = dict.fromkeys(STATUES, 0)
        province_agg[item['province']]['coord'] = item['coord']
        province_agg[item['province']]['country'] = item['country']

    province_agg[item['province']][item['status']] += 1
province = []
country = dict.fromkeys(STATUES, 0)
country_total = 0
for item in province_agg.iterkeys():
    res = ''
    total = 0
    for report_item in province_agg[item]:
        if report_item in ['coord', 'country']:
            continue

        res += '<span class="{}">{}:{}</span><br/> '.format(color.get(report_item, 'gray'), report_item,
                                                            province_agg[item][report_item])
        total += province_agg[item][report_item]
        country_total += province_agg[item][report_item]
        country[report_item] += province_agg[item][report_item]
    province_agg[item]['info'] = '<div dir="rtl"><h2>{}</h2><hr><br/>Total:{}<br/>{}</div>'.format(item, total, res)
    province_agg[item]['name'] = '{}'.format(item)
    province.append(province_agg[item])

res = ''
for item in country:
    if item == 'coord':
        continue
    res += '<span class="{}">{}:{}</span><br/> '.format(color.get(item, 'gray'), item,
                                                        country[item])

country['coord'] = [35.7211, 51.3995]
country['name'] = u'اطلاعات کل کشور '
country['info'] = u'<div dir="rtl"><h2>{}</h2><hr><br/>Total:{}<br/>{}</div>'.format(country['name'], country_total,
                                                                                     res)
print('good: {}, bad: {}'.format(good, bad))
result_json = json.dumps(result, ensure_ascii=not DEBUG, indent=4)
province_json = json.dumps(province, ensure_ascii=not DEBUG, indent=4)
country_json = json.dumps([country])

result_file = open(RESULT_FILE, 'w')
result_file.write('document.markers={detail:%s,province:%s,country:%s};' % (
    result_json, province_json, country_json))
result_file.close()
result_file = open(RESULT_FILE + 'on', 'w')
result_file.write('{"detail":%s,"province":%s,"country":%s}' % (
    result_json, province_json, country_json))
result_file.close()
