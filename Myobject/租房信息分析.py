"""
-*- coding:utf-8 -*-
@Time : 2020/12/11 0011 14:12
@Author : 陆一平
@File : 租房信息分析.py
@Software: PyCharm
"""
import pandas as pd
import numpy as np
from scipy.interpolate import lagrange
from pyecharts.charts import *
import pyecharts.options as opts
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot

# 输出可以全部显示
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

house_data = pd.read_excel('./anjuke.xlsx')
print(house_data.head(), house_data.shape)
print(house_data.columns)  # (3140, 12)
# 数据去重
house_data.drop_duplicates(subset=['标题', '价格', '交租方式', '户型', '楼层', '装修', '类型', '小区', '设施'], inplace=True, keep='last')
house_data.reindex(range(0, house_data.shape[0]))
print(house_data.shape)  # (2433, 12)

# 空值处理
# house_data.info()
# 其中发布时间有300空值，设施有117项空值
# 数据均为当日爬取，发布时间填为发布时间的众数
# print(house_data['发布时间'].mode())
house_data['发布时间'].fillna(value=house_data['发布时间'].mode(), inplace=True)
# 设施根据众数进行填充,众数共925，占据非空值的40%
# print(house_data['设施'].describe())
house_data['设施'].fillna(value=house_data['设施'].describe().top, inplace=True)
# house_data.info()    #(2433, 12)

# 根据小区提取出小区名称、区域、社区
house_data[['小区名称', '行政区', '社区']] = house_data['小区'].str.split('>').tolist()

# 删除不是1室的
mask1 = house_data['户型'].str.startswith('1室')
house_data.drop(axis=0, labels=house_data.loc[~mask1, :].index, inplace=True)

# 将面积改为数字
house_data['面积'] = house_data['面积'].str.split('平').str[0].astype(float)
# 成都市区行政区共13个，删除周边区县
# 锦江区、青羊区、金牛区、武侯区、成华区、新都区、郫都区、温江区、双流区、龙泉驿区、青白江区、成都高新区（非行政区）
drop_list = ['邛崃市', '崇州', '彭州', '金堂', '新津', '简阳', '都江堰']
for i in drop_list:
    mask = house_data['行政区'] == i
    house_data.drop(axis=0, labels=house_data.loc[mask, :].index, inplace=True)
print(house_data.shape)  # (2396, 15)


# 异常值处理,去掉小于500，大于5000的数据
def get_normal_score(val):
    low = 500
    high = 5000
    return val >= low and val <= high


mask2 = house_data['价格'].transform(get_normal_score)
house_data = house_data.loc[mask2, :]
print(house_data.shape)  # (2360, 15)

# 保存一份新数据
# writer = pd.ExcelWriter('./安居客租房信息表.xlsx')
# house_data.to_excel(excel_writer=writer,sheet_name='整租',index=False)
# writer.save()
# writer.close()


# 1.分析成都各区出租房数量
area_info = house_data['行政区'].value_counts()
area_list = [[k, int(v)] for k, v in zip(area_info.index, area_info.values)]
pie = Pie()
pie.add(series_name='各区出租房数量',
        data_pair=area_list,
        radius=["25%", "50%"],
        rosetype='area',
        )
# print(area_list)
pie.set_global_opts(legend_opts=opts.LegendOpts(type_='scroll',
                                                pos_left="25%",
                                                pos_right='25%'))

pie.set_series_opts(label_opts=opts.LabelOpts(
    formatter='{b}:{d}%'  # 数据项名称和百分比
))

# make_snapshot(snapshot, pie.render('./wad.html'), "./成都各区出租房数量.png")

# 2.查看成都租房的价格分布情况
# 使用箱线图
box = Boxplot()
box_data = house_data['价格'].values.tolist()

box.add_xaxis(xaxis_data=['成都租房'])
box.add_yaxis(series_name='价格', y_axis=box.prepare_data([box_data]))

box.set_global_opts(
    tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="shadow"),
    xaxis_opts=opts.AxisOpts(
        type_="category",
        boundary_gap=True,
        splitarea_opts=opts.SplitAreaOpts(is_show=False),
        splitline_opts=opts.SplitLineOpts(is_show=False),
    ),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        splitarea_opts=opts.SplitAreaOpts(
            is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1),
        ),
    ),
)
box.set_series_opts(tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}"))

# 3.各区租房价格对比
price = house_data.groupby('行政区')['价格'].mean().astype(int).sort_values(ascending=True)
# price_median = house_data.groupby('行政区')['价格'].median().astype(int).sort_values(ascending = False)
# print(price.index,'\n',price.values)
bar = Bar()
bar.add_xaxis(xaxis_data=price.index.tolist())
bar.add_yaxis(series_name='平均价格', y_axis=price.values.tolist())
bar.set_series_opts(label_opts=opts.LabelOpts(position='right',
                                              is_show=True))
bar.set_global_opts(xaxis_opts=opts.AxisOpts(name='价格',
                                             min_=500,
                                             max_=2500,
                                             split_number=4
                                             ),
                    yaxis_opts=opts.AxisOpts(name='区域',
                                             axislabel_opts=opts.LabelOpts(font_size=12))
                    )
bar.reversal_axis()

# 4.分析各区租房价格与面积的关系
print(house_data['面积'].describe())  # min10,max135
house_data['面积区间'] = pd.cut(house_data['面积'], bins=[10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 80, 140],
                            include_lowest=False)
price_square_area = house_data.groupby(by=['行政区', '面积区间'])['价格'].mean().reset_index()
price_square_area.sort_values(by=['价格', '面积区间'], ascending=[True, False], inplace=True)
price_square_area['面积区间'] = price_square_area['面积区间'].astype(str)
price_square_area.iloc[-1, 2] = 0
price_square_area['价格'].fillna(value=0, inplace=True)
price_square_area['价格'] = price_square_area['价格'].astype(int)
print(price_square_area)

area_list_v2 = sorted(list(set(price_square_area['行政区'].values.tolist())))
print(area_list_v2)
square_list = sorted(list(set(price_square_area['面积区间'].values.tolist())))
print(square_list)

item = {}
for i in square_list:
    mask3 = price_square_area['面积区间'] == i
    data1 = price_square_area.loc[mask3, :].sort_values(by='行政区')
    price_mean = data1['价格'].values.tolist()
    item[i] = price_mean
print(item)

timeline = Timeline()
bar2 = Bar()
bar2.add_xaxis(xaxis_data=area_list_v2)
def get_year_overlap_chart(square):
    bar2 = Bar()
    bar2.add_xaxis(xaxis_data=area_list_v2)
    bar2.add_yaxis(
        series_name="平均价格",
        y_axis=item[square],
        is_selected=True,
        label_opts=opts.LabelOpts(is_show=False),)
    bar2.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=14, interval=0,rotate=45,position='bottom'),
                                                  offset=0))
    return bar2
for square in square_list:
    timeline.add(get_year_overlap_chart(square=square), time_point="{}".format(square))
timeline.add_schema(is_auto_play=True, play_interval=1000,pos_left='5%',width='90%')


page = Page(layout=Page.DraggablePageLayout)
page.add(pie)
page.add(box)
page.add(bar)
page.add(timeline)
page.render('./租房信息.html')

