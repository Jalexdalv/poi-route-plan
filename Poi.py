class poi(object):
    # 经纬度x,y坐标
    x = 0
    y = 0
    # 城市(编号)
    city = str()
    city_id = str()
    # 景点名
    name = str()
    # 景点id
    id = str()
    # poi评分
    score = 0
    # poi评论
    comments = list()
    # 热度
    heat = 0
    # 评分列表
    score_list = list()
    # 游玩时间
    play_time = 0
    # 门票
    ticket = 0

    def __init__(self, x, y, name, id, city, city_id, score, score_list, heat, ticket, play_time, comments):
        self.x = x
        self.y = y
        self.id = id
        self.city = city
        self.name = name
        self.city_id = city_id
        self.score = score
        self.score_list = score_list
        self.heat = heat
        self.ticket = ticket
        self.play_time = play_time
        self.comments = comments
        # x,y,名称,id,城市名,城市id,评分,评分列表,热度,门票,游玩时间,评论

    def get_name(self):
        # 获取名字
        return self.name

    def get_coordinate(self):
        # 获取坐标
        return self.x, self.y

    def get_id(self):
        # 获取id
        return self.id

    def get_city(self):
        # 获取城市
        return self.city

    def get_city_id(self):
        # 获取城市编号
        return self.city_id

    def get_score(self):
        # 获取评分
        return self.score

    def get_comments(self):
        # 获取评论
        return self.comments

    def get_heat(self):
        # 获取热度
        return self.heat

    def get_play_time(self):
        # 获取游玩时间
        return self.play_time

    def get_ticket(self):
        # 获取门票
        return self.ticket

    def set_name(self, name):
        # 修改名字
        self.name = name

    def set_id(self, id):
        # 修改id
        self.id = id

    def set_coordinate(self, x, y):
        # 修改坐标
        self.x = x
        self.y = y

    def set_city(self, city):
        # 修改城市
        self.city = city

    def set_city_id(self, city_id):
        # 修改城市编号
        self.city_id = city_id

    def set_play_time(self, time):
        # 修改游玩时间
        self.play_time = time

    def set_ticket(self, ticket):
        # 修改门票
        self.ticket = ticket

    def add_score(self, score):
        # 增加一个评分
        self.score_list.append(score)

    def update_score(self):
        # 更新评分
        all_socre = 0
        for i in self.score_list:
            all_socre += i
        self.score = round(all_socre/len(self.score_list), 1)

    def add_comment(self, comment):
        # 添加评论
        self.comments.append(comment)

    def update_heat(self):
        # 更新热度　
        # 评论权重5  评分人数权重3
        self.heat = round(len(self.score_list)*5 + len(self.comments)*3)

    def show_info(self):
        return self.x, self.y, self.name, self.id, self.city, self.city_id, self.score, self.score_list, self.heat, \
               self.ticket, self.play_time, self.comments

