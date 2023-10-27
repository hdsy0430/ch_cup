# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：pic.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/9/25 21:38 
'''
import matplotlib.pyplot as plt

# 学习plt画各种图

#设置字体的默认参数避免乱码
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

#1 条形图

a = ["战狼2","速度与激情8","功夫瑜伽","西游伏妖篇","变形金刚5：最后的骑士","摔跤吧！爸爸","加勒比海盗5：死无对证","金刚：骷髅岛","极限特工：终极回归","生化危机6：终章","乘风破浪","神偷奶爸3","智取威虎山","大闹天竺","金刚狼3：殊死一战","蜘蛛侠：英雄归来","悟空传","银河护卫队2","情圣","新木乃伊",]

b=[56.01,26.94,17.53,16.49,15.45,12.96,11.8,11.61,11.28,11.12,10.49,10.3,8.75,7.55,7.32,6.99,6.88,6.86,6.58,6.23]
plt.figure(figsize=(20,10),dpi=150)
# #水平条形图用barh
# plt.barh(y=range(len(a)),width=b,height=0.5,color="green")     #width的值可以是固定值，也可以是与y值相同长度的序列
#竖直条形图用bar
plt.bar(x=range(len(a)),height=b,width=0.3)
plt.xticks(ticks=range(len(a)),labels=a,rotation = 90)
# #设置y轴刻度以及标签用yticks
# plt.yticks(ticks=range(len(a)),labels=a)
# plt.grid()  #添加网格线
plt.show()

#2 散点图
# y_3 = [11,17,16,11,12,11,12,6,6,7,8,9,12,15,14,17,18,21,16,17,20,14,15,15,15,19,21,22,22,22,23]
# y_10 = [26,26,28,19,21,17,16,19,18,20,20,19,22,23,17,20,21,20,22,15,11,15,5,13,17,10,11,13,12,13,6]
# x_3 = range(1,32)
# x_10 = range(61,92)
# plt.figure(figsize=(18,8),dpi=80)
# #散点图用scatter
# plt.scatter(x=x_3,y=y_3,label="3月")
# plt.scatter(x_10,y_10,label="10月")
# x = list(x_3)+list(x_10)
# x_ticks = ["3月{}".format(i) for i in x_3]
# x_ticks += ["10月{}".format(i-60) for i in x_10 ]
# plt.xticks(ticks=x[::3],labels=x_ticks[::3],rotation = 45)
# plt.title("weather")
# plt.xlabel("date")
# plt.ylabel("warm")
# plt.legend(loc = 'upper left')  #添加图例解释标签
# plt.show()
