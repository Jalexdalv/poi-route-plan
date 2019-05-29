# from urllib import request
# import json
#
#
# amap_web_key = 'b745dc3a2297df3929483a9c6a161289'
# poi_search_url = "https://restapi.amap.com/v3/distance?"
#
#
# def distance(a, b):
#     req_url = poi_search_url + 'origins=' + str(a[0])+','+str(a[1]) + '&destination=' + str(b[0])+','+str(b[1]) +
#               '&output=json&key=' + amap_web_key
#     data = str()
#     with request.urlopen(req_url) as f:
#         data = f.read()
#         data = data.decode('utf-8')
#     temp_data = json.loads(data)
#     return temp_data['results'][0]['distance'], temp_data['results'][0]['duration']


from math import radians, cos, sin, asin, sqrt


def haversine(a, b):
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [float(a[0]), float(a[1]), float(b[0]), float(b[1])])
    # haversine 公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return int(c * r * 1000)
