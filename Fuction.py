import csv
import Poi
import random
import Distance


def get_pois_cityname():
    # 获取poi的城市名称与城市id的映射
    with open('pois\\' + 'list' + '.txt', 'r') as f:
        line = f.readline()
        poi_name_list = list()
        while line:
            s = line.split(' ')
            poi_name_list.append({s[0].strip():s[1].strip()})  # {城市名：城市id}
            line = f.readline()  # 继续读取下一行
        print(poi_name_list)
        return poi_name_list


def search(keyword, poi_name_list):
    # 搜索
    for i in poi_name_list:
        if keyword in i:
            return True, i[keyword]  # 返回城市编码
        else:
            continue
    return False


def load_pois_data(city_id):
    pois = list()
    comments = list()
    with open('pois\\'+city_id+'\\'+city_id+'comments.csv', 'r') as f:
        comments_read = csv.reader(f)
        for cr in comments_read:
            comments.append(cr)
    with open('pois\\'+city_id+'\\'+city_id+'.csv', 'r') as f:
        csv_read = csv.reader(f)
        for cr in csv_read:
            temp = list()
            try:
                for i in cr[7].split(','):
                    temp.append(float(i))
            except:
                pass
            comment = list()
            for cs in comments:
                if cs[0] == cr[3]:
                    comment = cs
                    break
            poi = Poi.poi(cr[0], cr[1], cr[2], cr[3], cr[4], cr[5], cr[6], temp, cr[8], cr[9], cr[10], comment)
            pois.append(poi)
    return pois


def router_plan(pois, time, sign):
    # 根据游玩时间选定兴趣点，评分以及热度综合从高到低
    # 1天的实际时间10小时，输入1天则计算实际游玩时间+路程时间10小时
    # sign为0则使用评分优先算法，sign为1使用热度优先算法
    # 评分优先算法：优先选择评分高的POI点，评分从最高->最低开始累加游玩时间
    # 最短路径算法：这个算法比较类似与著名的TSP旅行商问题
    router = list()
    show_text = str()
    if sign == 0:
        router = score_first(pois, time)
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(router[2],2)) + 'KM' + ' 总耗时：' + str(
            round(router[3], 2)) + '小时' + '\n'
        i = 0
        for r in router[0]:
            if i == 0:
                text = '\n' + router[1][r[0]].get_name() + ' 景点评分：' + router[1][r[0]].get_score() + ' 景点游玩时间：' + \
                       router[1][r[0]].get_play_time() + '小时' + '\n'
                text = text + router[1][r[0]].get_name() + '--->' + router[1][r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + router[1][r[0]].get_score()
                text = text + ' 游玩时间：' + router[1][r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = router[1][r[0]].get_name() + '--->' + router[1][r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + router[1][r[0]].get_score()
                text = text + ' 游玩时间：' + router[1][r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
    elif sign == 1:
        router = heat_first(pois, time)
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(router[2],2)) + 'KM' + ' 总耗时：' + str(
            round(router[3], 2)) + '小时' + '\n'
        i = 0
        for r in router[0]:
            if i == 0:
                text = '\n' + router[1][r[0]].get_name() + ' 景点热度：' + router[1][r[0]].get_heat() + ' 景点游玩时间：' + \
                       router[1][r[0]].get_play_time() + '小时' + '\n'
                text = text + router[1][r[0]].get_name() + '--->' + router[1][r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + router[1][r[0]].get_heat()
                text = text + ' 游玩时间：' + router[1][r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = router[1][r[0]].get_name() + '--->' + router[1][r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + router[1][r[0]].get_heat()
                text = text + ' 游玩时间：' + router[1][r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
    return show_text,router


def score_first(pois, time):
    # 评分优先
    # 对所有poi按评分排序
    time = time*10
    pois = sorted(pois, key=lambda poi: float(poi.get_score()), reverse=True)  #　根据评分排序
    sum_time = 0   # 总时间
    target_poi = list()  # 得出的可选poi
    for poi in pois:
        # 首先假设所有时间都用来游览景点
        target_poi.append(poi)
        sum_time += int(poi.get_play_time())
        if sum_time == time:
            break
        elif sum_time > time:
            sum_time -= int(poi.get_play_time())
            target_poi.pop()
            break
        else:
            continue
    # 递归开始
    router = find_shortest(target_poi, time, sum_time)
    return router


def find_shortest(target_poi, time, sum_time):
    j = 0
    sign_list = dict()  # poi-序号映射表
    for i in target_poi:
        sign_list[j] = i
        j += 1
    m = 0
    n = 0
    dis = []
    for m in range(0, j):
        dis.append([])
        for n in range(0, j):
            if m == n:
                continue
            else:
                # m->n 的距离
                temp = Distance.haversine(target_poi[m].get_coordinate(), target_poi[n].get_coordinate())
                # print(temp)
                dis[m].append([n, temp])
    router = list()
    all_dis = 0  # 总路径长度
    all_router_time = 0 # 总路程时间

    go_list = []
    k = 0
    for i in range(0, j-1):
        start = k
        k, t, shortest_dis = tsp(go_list, dis, k)
        all_dis += shortest_dis/1000  # 公里
        # 按平均60KM/H计算时间
        all_router_time += (shortest_dis/1000)/60  # 小时
        router.append([start, k, round(shortest_dis/1000, 2), round((shortest_dis/1000)/60, 2)])  # [0,1,dis,time]
    # print(all_dis)
    # print(all_router_time)
    # print(router)
    if all_router_time+sum_time > time:
        s = target_poi.pop()
        for i in target_poi:
            print(i.show_info())
        return find_shortest(target_poi, time, sum_time-int(s.get_play_time()))
    else:
        return router, sign_list, all_dis, all_router_time+sum_time


def tsp(go_list, dis, index):
    # 记录已经去过的poi
    t = sorted(dis[index], key=lambda d: int(d[1]))  # 按距离进行排序
    l = 0
    while t[l][0] in go_list:
        l += 1
    go_list.append(index)
    shortest_dis = t[l][1]
    k = t[l][0]
    return k, t, shortest_dis


def heat_first(pois, time):
    # 热度优先
    # 对所有poi按热度排序
    time = time * 10
    pois = sorted(pois, key=lambda poi: float(poi.get_heat()), reverse=True)  # 根据热度排序
    sum_time = 0  # 总时间
    target_poi = list()  # 得出的可选poi
    for poi in pois:
        # 首先假设所有时间都用来游览景点
        target_poi.append(poi)
        sum_time += int(poi.get_play_time())
        if sum_time == time:
            break
        elif sum_time > time:
            sum_time -= int(poi.get_play_time())
            target_poi.pop()
            break
        else:
            continue
    # 递归开始
    router = find_shortest(target_poi, time, sum_time)
    return router


def add_comment(poi, comment):
    # 添加评论
    poi.add_comment(comment)
    poi.update_heat()


def add_score(poi, score):
    # 添加评分
    poi.add_score(score)
    poi.update_score()
    poi.update_heat()


def add_poi_to_router(sub_poi, poi, sign):
    target_poi = list()
    k = 0
    for i in sub_poi[0]:
        if k == 0:
            target_poi.append(sub_poi[1][i[0]])
            target_poi.append(sub_poi[1][i[1]])
        else:
            target_poi.append(sub_poi[1][i[1]])
        k+=1
    target_poi.append(poi)
    sum_time = 0
    for i in target_poi:
            sum_time = sum_time + int(i.get_play_time())
    j = 0
    sign_list = dict()  # poi-序号映射表
    for i in target_poi:
        sign_list[j] = i
        j += 1
    m = 0
    n = 0
    dis = []
    for m in range(0, j):
        dis.append([])
        for n in range(0, j):
            if m == n:
                continue
            else:
                # m->n 的距离
                temp = Distance.haversine(target_poi[m].get_coordinate(), target_poi[n].get_coordinate())
                # print(temp)
                dis[m].append([n, temp])
    router = list()
    all_dis = 0  # 总路径长度
    all_router_time = 0  # 总路程时间

    go_list = []
    k = 0
    for i in range(0, j - 1):
        start = k
        k, t, shortest_dis = tsp(go_list, dis, k)
        all_dis += shortest_dis / 1000  # 公里
        # 按平均60KM/H计算时间
        all_router_time += (shortest_dis / 1000) / 60  # 小时
        router.append([start, k, round(shortest_dis / 1000, 2), round((shortest_dis / 1000) / 60, 2)])  # [0,1,dis,time]

    if sign == 0:
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(all_dis, 2)) + 'KM' + ' 总耗时：' + str(
            round(all_router_time+sum_time, 2)) + '小时' + '\n'
        i = 0
        for r in router:
            if i == 0:
                text = '\n' + sign_list[r[0]].get_name() + ' 景点评分：' + sign_list[r[0]].get_score() + ' 景点游玩时间：' + \
                       sign_list[r[0]].get_play_time() + '小时' + '\n'
                text = text + sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + sign_list[r[0]].get_score()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + sign_list[r[0]].get_score()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
        return router, sign_list, all_dis, all_router_time + sum_time, show_text
    else:
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(all_dis, 2)) + 'KM' + ' 总耗时：' + str(
            round(all_router_time + sum_time, 2)) + '小时' + '\n'
        i = 0
        for r in router:
            if i == 0:
                text = '\n' + sign_list[r[0]].get_name() + ' 景点热度：' + sign_list[r[0]].get_heat() + ' 景点游玩时间：' + \
                       sign_list[r[0]].get_play_time() + '小时' + '\n'
                text = text + sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + sign_list[r[0]].get_heat()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + sign_list[r[0]].get_heat()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
        return router, sign_list, all_dis, all_router_time + sum_time, show_text


def del_poi_in_router(sub_poi, poi, sign):
    target_poi = list()
    k = 0
    for i in sub_poi[0]:
        if k == 0:
            target_poi.append(sub_poi[1][i[0]])
            target_poi.append(sub_poi[1][i[1]])
        else:
            target_poi.append(sub_poi[1][i[1]])
        k += 1
    p = 0
    for i in target_poi:
        if i.get_id() == poi.get_id():
            del target_poi[p]
        p+=1
    print(target_poi)
    sum_time = 0
    for i in target_poi:
        sum_time = sum_time + int(i.get_play_time())
    j = 0
    sign_list = dict()  # poi-序号映射表
    for i in target_poi:
        sign_list[j] = i
        j += 1
    m = 0
    n = 0
    dis = []
    for m in range(0, j):
        dis.append([])
        for n in range(0, j):
            if m == n:
                continue
            else:
                # m->n 的距离
                temp = Distance.haversine(target_poi[m].get_coordinate(), target_poi[n].get_coordinate())
                # print(temp)
                dis[m].append([n, temp])
    router = list()
    all_dis = 0  # 总路径长度
    all_router_time = 0  # 总路程时间

    go_list = []
    k = 0
    for i in range(0, j - 1):
        start = k
        k, t, shortest_dis = tsp(go_list, dis, k)
        all_dis += shortest_dis / 1000  # 公里
        # 按平均60KM/H计算时间
        all_router_time += (shortest_dis / 1000) / 60  # 小时
        router.append([start, k, round(shortest_dis / 1000, 2), round((shortest_dis / 1000) / 60, 2)])  # [0,1,dis,time]

    if sign == 0:
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(all_dis, 2)) + 'KM' + ' 总耗时：' + str(
            round(all_router_time + sum_time, 2)) + '小时' + '\n'
        i = 0
        for r in router:
            if i == 0:
                text = '\n' + sign_list[r[0]].get_name() + ' 景点评分：' + sign_list[r[0]].get_score() + ' 景点游玩时间：' + \
                       sign_list[r[0]].get_play_time() + '小时' + '\n'
                text = text + sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + sign_list[r[0]].get_score()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + sign_list[r[0]].get_score()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
        return router, sign_list, all_dis, all_router_time + sum_time, show_text
    else:
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(all_dis, 2)) + 'KM' + ' 总耗时：' + str(
            round(all_router_time + sum_time, 2)) + '小时' + '\n'
        i = 0
        for r in router:
            if i == 0:
                text = '\n' + sign_list[r[0]].get_name() + ' 景点热度：' + sign_list[r[0]].get_heat() + ' 景点游玩时间：' + \
                       sign_list[r[0]].get_play_time() + '小时' + '\n'
                text = text + sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + sign_list[r[0]].get_heat()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + sign_list[r[0]].get_heat()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
        return router, sign_list, all_dis, all_router_time + sum_time, show_text


def change_poi_in_router(sub_poi, poi, new_poi,sign):
    target_poi = list()
    k = 0
    for i in sub_poi[0]:
        if k == 0:
            target_poi.append(sub_poi[1][i[0]])
            target_poi.append(sub_poi[1][i[1]])
        else:
            target_poi.append(sub_poi[1][i[1]])
        k += 1
    p = 0
    for i in target_poi:
        if i.get_id() == poi.get_id():
            del target_poi[p]
        p += 1
    target_poi.append(new_poi)
    sum_time = 0
    for i in target_poi:
        sum_time = sum_time + int(i.get_play_time())
    j = 0
    sign_list = dict()  # poi-序号映射表
    for i in target_poi:
        sign_list[j] = i
        j += 1
    m = 0
    n = 0
    dis = []
    for m in range(0, j):
        dis.append([])
        for n in range(0, j):
            if m == n:
                continue
            else:
                # m->n 的距离
                temp = Distance.haversine(target_poi[m].get_coordinate(), target_poi[n].get_coordinate())
                # print(temp)
                dis[m].append([n, temp])
    router = list()
    all_dis = 0  # 总路径长度
    all_router_time = 0  # 总路程时间

    go_list = []
    k = 0
    for i in range(0, j - 1):
        start = k
        k, t, shortest_dis = tsp(go_list, dis, k)
        all_dis += shortest_dis / 1000  # 公里
        # 按平均60KM/H计算时间
        all_router_time += (shortest_dis / 1000) / 60  # 小时
        router.append([start, k, round(shortest_dis / 1000, 2), round((shortest_dis / 1000) / 60, 2)])  # [0,1,dis,time]

    if sign == 0:
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(all_dis, 2)) + 'KM' + ' 总耗时：' + str(
            round(all_router_time + sum_time, 2)) + '小时' + '\n'
        i = 0
        for r in router:
            if i == 0:
                text = '\n' + sign_list[r[0]].get_name() + ' 景点评分：' + sign_list[r[0]].get_score() + ' 景点游玩时间：' + \
                       sign_list[r[0]].get_play_time() + '小时' + '\n'
                text = text + sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + sign_list[r[0]].get_score()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点评分：' + sign_list[r[0]].get_score()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
        return router, sign_list, all_dis, all_router_time + sum_time, show_text
    else:
        show_text = '线路规划结果如下：' + '\n' + '总路程：' + str(round(all_dis, 2)) + 'KM' + ' 总耗时：' + str(
            round(all_router_time + sum_time, 2)) + '小时' + '\n'
        i = 0
        for r in router:
            if i == 0:
                text = '\n' + sign_list[r[0]].get_name() + ' 景点热度：' + sign_list[r[0]].get_heat() + ' 景点游玩时间：' + \
                       sign_list[r[0]].get_play_time() + '小时' + '\n'
                text = text + sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + sign_list[r[0]].get_heat()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            else:
                text = sign_list[r[0]].get_name() + '--->' + sign_list[r[1]].get_name() + ' 距离：' + str(
                    r[2]) + 'KM' + ' 路程时间：' + str(r[3]) + '小时'
                text = text + ' 景点热度：' + sign_list[r[0]].get_heat()
                text = text + ' 游玩时间：' + sign_list[r[1]].get_play_time() + '小时' + '\n'
                show_text += text
            i += 1
        show_text += '祝您旅途愉快！'
        return router, sign_list, all_dis, all_router_time + sum_time, show_text


def Test():
    # 生成测试poi数据
    score_list = list()
    all_score = 0
    ran_nums = random.randint(0,10)
    for i in range(0, ran_nums):
        ran = round(random.uniform(0, 5), 1)
        score_list.append(str(ran))
        all_score += ran
    if all_score == 0:
        avg = 0
    else:
        avg = round(all_score/ran_nums, 1)
    heat = round(ran_nums*5)
    ticket = random.randint(20, 300)
    play_time = random.randint(1, 5)
    # 返回评分、评分列表、热度、门票、建议游玩时间
    return avg, ','.join(score_list), heat, ticket, play_time


# if __name__ == '__main__':
# #     # 运行Test
# #     print(Test())

