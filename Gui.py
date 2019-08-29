import tkinter
import Fuction
import Poi
from tkinter import ttk
from tkinter import messagebox


class Gui(object):
    def __init__(self, master):
        self.master = master
        self.router = list()
        self.pois = list()
        self.sign = 0
        # 上方输入区域
        self.topFrame = tkinter.Frame(padx=5, pady=5)
        self.topFrame.pack()
        tkinter.Label(self.topFrame, text='输入城市', font=16).grid(column=1, row=1, sticky=tkinter.E)
        # 搜索输入栏
        self.search_input = tkinter.Entry(self.topFrame, width=30)
        self.search_input.grid(column=2, row=1, sticky=tkinter.W)
        tkinter.Label(self.topFrame, text='输入旅游时间/天', font=16).grid(column=1, row=2, sticky=tkinter.E)
        # 搜索输入栏
        self.time_input = tkinter.Entry(self.topFrame, width=20)
        self.time_input.grid(column=2, row=2, sticky=tkinter.W, pady=10)
        # 选择优先方式
        self.ch_box1_text = tkinter.StringVar()
        self.ch_box1 = ttk.Combobox(self.topFrame, width=15, font=16, textvariable=self.ch_box1_text)
        self.ch_box1['values'] = ('评分优先', '热度优先')  # 设置下拉列表的值
        self.ch_box1.grid(column=3, columnspan=3, row=1, pady=10, padx=20)
        self.ch_box1.current(0)

        # 搜索按钮
        self.search_button = tkinter.Button(self.topFrame, command=self.start_search, text="开始规划路线", font=16)
        self.search_button.grid(column=3, row=2, sticky=tkinter.E, padx=30,ipadx=10)

        # 中部显示区域
        self.showFrame = tkinter.Frame(padx=10, pady=5)
        self.showFrame.pack()
        tkinter.Label(self.showFrame, text='路线规划结果', font=16).pack()
        self.ShowArea = tkinter.Scrollbar(self.showFrame)
        self.ShowArea.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.ShowData = tkinter.Text(self.showFrame, width=60, height=8, font=16, state=tkinter.DISABLED,
                                     yscrollcommand=self.ShowArea.set)
        self.ShowData.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.ShowArea.config(command=self.ShowData.yview)

        # 下方操作区域
        self.operationFrame = tkinter.Frame(padx=10, pady=10)
        self.operationFrame.pack()
        tkinter.Label(self.operationFrame, text='路线修改', font=16).grid(column=1, row=1, columnspan=4)
        tkinter.Label(self.operationFrame, text='★选择要添加的poi', font=16).grid(column=1, row=2, sticky=tkinter.W,padx=10)
        # 选择增加的poi
        self.ch_box2_text = tkinter.StringVar()
        self.ch_box2 = ttk.Combobox(self.operationFrame, width=15, font=16, textvariable=self.ch_box2_text)
        self.ch_box2['values'] = ('sss','aaa')  # 设置下拉列表的值
        self.ch_box2.grid(column=2, row=2, pady=10, padx=20)
        # self.ch_box2.current(0)
        # 增加按钮
        self.add_button = tkinter.Button(self.operationFrame, command=self.start_add, text="增添", font=16)
        self.add_button.grid(column=3, row=2, sticky=tkinter.E, padx=20,ipadx=10)

        tkinter.Label(self.operationFrame, text='★选择要删除的poi', font=16).grid(column=1, row=4, sticky=tkinter.W, padx=10)
        # 选择删除的poi
        self.ch_box3_text = tkinter.StringVar()
        self.ch_box3 = ttk.Combobox(self.operationFrame, width=15, font=16, textvariable=self.ch_box3_text)
        self.ch_box3['values'] = ()  # 设置下拉列表的值
        self.ch_box3.grid(column=2, row=4, pady=10, padx=20)
        # self.ch_box3.current(0)
        # 删除按钮
        self.del_button = tkinter.Button(self.operationFrame, command=self.start_del, text="删除", font=16)
        self.del_button.grid(column=3, row=4, sticky=tkinter.E, padx=20, ipadx=10)

        tkinter.Label(self.operationFrame, text='★选择要修改的poi', font=16).grid(column=1, row=5, sticky=tkinter.W, padx=10)
        # 选择修改的poi
        self.ch_box4_text = tkinter.StringVar()
        self.ch_box4 = ttk.Combobox(self.operationFrame, width=15, font=16, textvariable=self.ch_box4_text)
        self.ch_box4['values'] = ()  # 设置下拉列表的值
        self.ch_box4.grid(column=2, row=5, pady=10,padx=20)
        # self.ch_box4.current(0)

        tkinter.Label(self.operationFrame, text='  选择修改后的结果', font=16).grid(column=1, row=6, sticky=tkinter.W, padx=10)
        # 选择修改成的poi
        self.ch_box5_text = tkinter.StringVar()
        self.ch_box5 = ttk.Combobox(self.operationFrame, width=15, font=16, textvariable=self.ch_box5_text)
        self.ch_box5['values'] = ()  # 设置下拉列表的值
        self.ch_box5.grid(column=2, row=6, pady=10, padx=20)
        # self.ch_box5.current(0)
        # 修改按钮
        self.change_button = tkinter.Button(self.operationFrame, command=self.start_change, text="修改", font=16)
        self.change_button.grid(column=3, row=6, sticky=tkinter.E, padx=20, ipadx=10)

        # 评价区域
        self.commentFrame = tkinter.Frame(padx=10)
        self.commentFrame.pack()
        tkinter.Label(self.commentFrame, text='评价poi', font=16).grid(column=1, row=1, columnspan=4)
        tkinter.Label(self.commentFrame, text='选择一个poi', font=16).grid(column=1, row=2, columnspan=2,padx=20)
        # 选择一个的poi
        self.ch_box6_text = tkinter.StringVar()
        self.ch_box6 = ttk.Combobox(self.commentFrame, width=15, font=16, textvariable=self.ch_box6_text)
        self.ch_box6['values'] = ()  # 设置下拉列表的值
        self.ch_box6.grid(column=2, row=2, pady=10, padx=20,columnspan=3)
        # self.ch_box6.current(0)

        tkinter.Label(self.commentFrame, text='★输入评论内容', font=16).grid(column=1, row=3, sticky=tkinter.W, padx=10)
        self.comment_input = tkinter.Entry(self.commentFrame, width=30)
        self.comment_input.grid(column=2, row=3, sticky=tkinter.W)
        self.comment_button = tkinter.Button(self.commentFrame, command=self.start_comment,text="评论", font=16)
        self.comment_button.grid(column=3, row=3, sticky=tkinter.E, padx=20, ipadx=10,pady=5)
        tkinter.Label(self.commentFrame, text='★输入您的评分', font=16).grid(column=1, row=4, sticky=tkinter.W, padx=10)
        self.score_input = tkinter.Entry(self.commentFrame, width=20)
        self.score_input.grid(column=2, row=4, sticky=tkinter.W)
        self.score_button = tkinter.Button(self.commentFrame, command=self.start_score,text="打分", font=16)
        self.score_button.grid(column=3, row=4, sticky=tkinter.E, padx=20, ipadx=10,pady=5)
        # 未实现的功能：保存评论以及评分
        # master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_search(self):
        self.ShowData.delete(0.0, tkinter.END)
        search_way = self.ch_box1_text.get().strip()
        search_city = self.search_input.get().strip()
        sign = 0
        time = self.time_input.get().strip()
        if search_city == '':
            messagebox.showinfo('警告', '城市名不能输入为空！')
        else:
            if time == '':
                messagebox.showinfo('警告', '旅行时间不能输入为空！')
            else:
                if not time.isdigit():
                    messagebox.showinfo('警告', '旅行时间必须输入正整数(例如1,2,3,4...)！')
                else:
                    if not Fuction.search(search_city, Fuction.get_pois_cityname()) == False:
                        pois = Fuction.load_pois_data(Fuction.search(search_city, Fuction.get_pois_cityname())[1])
                        if search_way == '评分优先':
                            router_text,router = Fuction.router_plan(pois, int(time), 0)
                            sign = 0
                        else:
                            router_text,router = Fuction.router_plan(pois, int(time), 1)
                            sign = 1
                        self.ShowData.config(state=tkinter.NORMAL)
                        self.ShowData.insert(tkinter.END, router_text)
                        self.ShowData.see(tkinter.END)
                        self.router = router
                        self.pois = pois
                        self.update_combox()
                        self.sign = sign
                    else:
                        messagebox.showinfo('警告', '您搜索的城市不存在，请等待系统的进一步更新！')

    def update_combox(self):
        not_add_list = list()
        router_list = list()
        k = 0
        for i in self.router[0]:
            if k == 0:
                router_list.append(self.router[1][i[0]].get_id())
                not_add_list.append(self.router[1][i[0]].get_name())
            router_list.append(self.router[1][i[1]].get_id())
            not_add_list.append(self.router[1][i[1]].get_name())
            k += 1
        add_list = list()
        for i in self.pois:
            if i.get_id() in router_list:
                continue
            else:
                add_list.append(i.get_name())
        self.ch_box2['values'] = tuple(add_list)
        self.ch_box3['values'] = tuple(not_add_list)
        self.ch_box4['values'] = tuple(not_add_list)
        self.ch_box5['values'] = tuple(add_list)
        self.ch_box6['values'] = tuple(not_add_list)

    def start_add(self):
        self.ShowData.delete(0.0, tkinter.END)
        poi = self.pois[0]
        for i in self.pois:
            if i.get_name() == self.ch_box2.get():
                poi = i
        router = Fuction.add_poi_to_router(self.router, poi, self.sign)
        self.ShowData.config(state=tkinter.NORMAL)
        self.ShowData.insert(tkinter.END, router[4])
        self.ShowData.see(tkinter.END)
        self.router = router
        self.update_combox()
        self.ch_box2.current(0)

    def start_del(self):
        self.ShowData.delete(0.0, tkinter.END)
        poi = self.pois[0]
        for i in self.pois:
            if i.get_name() == self.ch_box3.get():
                poi = i
        router = Fuction.del_poi_in_router(self.router, poi, self.sign)
        self.ShowData.config(state=tkinter.NORMAL)
        self.ShowData.insert(tkinter.END, router[4])
        self.ShowData.see(tkinter.END)
        self.router = router
        self.update_combox()
        self.ch_box3.current(0)

    def start_change(self):
        self.ShowData.delete(0.0, tkinter.END)
        poi = self.pois[0]
        new_poi = self.pois[0]
        for i in self.pois:
            if i.get_name() == self.ch_box4.get():
                poi = i
            elif i.get_name() == self.ch_box5.get():
                new_poi = i
        router = Fuction.change_poi_in_router(self.router, poi, new_poi, self.sign)
        self.ShowData.config(state=tkinter.NORMAL)
        self.ShowData.insert(tkinter.END, router[4])
        self.ShowData.see(tkinter.END)
        self.router = router
        self.update_combox()
        self.ch_box4.current(0)
        self.ch_box5.current(0)

    def start_comment(self):
        poi = self.pois[0]
        for i in self.pois:
            if i.get_name() == self.ch_box5.get():
                poi = i
        Fuction.add_comment(poi, self.comment_input.get().strip())

    def start_score(self):
        poi = self.pois[0]
        for i in self.pois:
            if i.get_name() == self.ch_box6.get():
                poi = i
        Fuction.add_score(poi, self.score_input.get().strip())

    # 未实现的功能：保存评论以及评分
    # def on_closing(self):
    #     messagebox.showinfo('提示', '保存成功')
    #     self.master.destroy()


root = tkinter.Tk()
root.title("旅行路线规划")
root.wm_minsize(500, 620)
# 进入消息循环
app = Gui(root)
root.mainloop()
