'''
本文件的功能为：
高德地图poi数据采集
存入CSV文件
'''

from urllib.parse import quote
from urllib import request
import json
import csv
import os
import Fuction

amap_web_key = 'b745dc3a2297df3929483a9c6a161289'
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"

cityname = '哈尔滨'
city_id = '0451'
classes = '风景名胜'


# 根据城市名称和分类关键字获取poi数据
def getpois(city, keywords):
    i = 1
    poi_list = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(city, keywords, i)
        print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        hand(poi_list, result)
        i = i + 1
    return poi_list


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


def save_pois(pois):
    # 保存poi信息
    with open('C:\\Users\\jalex\\PycharmProjects\\RPA\\pois\\'+city_id+'\\'+city_id+'.csv', 'w', newline='') as f:
        csv_write = csv.writer(f)
        for poi in pois:
            csv_write.writerow()
        print("写入csv文件成功")
    with open('C:\\Users\\jalex\\PycharmProjects\\RPA\\pois\\'+city_id+'\\'+city_id+'comments.csv', 'w',
              newline=''):
        csv_write = csv.writer(f)
        csv_write.writerow()


def write_to_csv(poilist, cityname, city_id):
    os.makedirs('C:\\Users\\jalex\\PycharmProjects\\RPA\\pois\\'+city_id)
    with open('C:\\Users\\jalex\\PycharmProjects\\RPA\\pois\\'+city_id+'\\'+city_id+'.csv', 'w', newline='') as f:
        csv_write = csv.writer(f)
        for poi in poilist:
            test_data = Fuction.Test()
            # print(test_data)
            csv_write.writerow([str(poi['location'].split(",")[0]), str(poi['location'].split(",")[1]),
                                poi['name'], poi['id'], cityname, str(city_id), test_data[0], test_data[1],
                                test_data[2], test_data[3], test_data[4]])
        print("写入csv文件成功")
    with open('C:\\Users\\jalex\\PycharmProjects\\RPA\\pois\\'+city_id+'\\'+city_id+'comments.csv', 'w', newline='') as f:
        # 建立评论文件
        # id 评论...
        print("创建评论文件成功")
    # x,y,名称,id,城市名,城市id,评分,评分列表,热度,门票,游玩时间


def write_poiname_to_txt(cityname, city_id):
    with open('C:\\Users\\jalex\\PycharmProjects\\RPA\\pois\\'+'list.txt', 'a+') as f:
        f.write(cityname+' '+city_id+'\n')
        print("写入城市列表文件成功")


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true&children=1' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = str()
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


if __name__ == '__main__':
    classes_all_pois = []
    pois_area = getpois(cityname, classes)
    classes_all_pois.extend(pois_area)
    write_to_csv(classes_all_pois, cityname, city_id)
    write_poiname_to_txt(cityname, city_id)
    print("写入csv文件成功")

