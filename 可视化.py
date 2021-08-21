# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 20:56:35 2021

@author: 曹进辉
"""
from pyecharts import options as opts
from pyecharts.charts import Line, Grid, Page
import os
import pandas as pd
import numpy as np
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

fund_data = pd.read_csv('data/fund_data.csv', dtype = {'code':str})

fund_code = {'160106', '160221', '002907', '001856', '011103', '001553','004854', '161726', '163406', '162605', '006308', '519196',
             '004224', '162703', '001009', '003834', '000751', '003095', '009225', '005827', '002692', '320007', '008087', '010253',
             '001500', '001475', '001838', '167301', '161620', '160639', '164403', '161725', '001156'}

code_name = {'001009': '上投摩根安全战略股票',
 '161725': '招商中证白酒指数(LOF)A',
 '006308': '汇添富全球消费混合人民币A',
 '010253': '兴银中证500指数增强A',
 '004224': '南方军工改革灵活配置混合A',
 '005827': '易方达蓝筹精选混合',
 '002907': '南方中证500量化增强C',
 '009225': '天弘中证中美互联网(QDII)A',
 '001156': '申万菱信新能源汽车混合',
 '167301': '方正富邦保险主题指数',
 '000751': '嘉实新兴产业股票',
 '001838': '国投瑞银国家安全混合',
 '164403': '前海开源沪港深农业混合',
 '002692': '富国创新科技混合A',
 '519196': '万家新兴蓝筹灵活配置混合',
 '160221': '国泰国证有色金属行业指数(LOF)',
 '001500': '泓德远见回报混合',
 '162605': '景顺长城鼎益混合(LOF)',
 '004854': '广发中证全指汽车指数A',
 '161620': '融通核心价值混合',
 '001475': '易方达国防军工混合',
 '161726': '招商国证生物医药指数(LOF)A',
 '001553': '天弘中证证券保险C',
 '003834': '华夏能源革新股票A',
 '320007': '诺安成长混合',
 '008087': '华夏中证5G通信主题ETF联接C',
 '160106': '南方高增长混合(LOF)',
 '162703': '广发小盘成长混合(LOF)A',
 '160639': '鹏华中证高铁产业指数(LOF)',
 '001856': '易方达环保主题混合',
 '011103': '天弘中证光伏产业指数C',
 '163406': '兴全合润混合(LOF)',
 '003095': '中欧医疗健康混合A'}

background_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
)
area_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
)
# flag = True
page = Page(layout=Page.SimplePageLayout)  # 简单布局
for code in fund_code:
    new_data = fund_data[fund_data['code'] == code]
    new_data = new_data.iloc[-200:,]
    date = list(new_data.iloc[-200:,]['date'].values)
    new_data['MACD'] = np.around(new_data['MACD'].values, decimals=3)
    new_data['MACDsignal']= np.around(new_data['MACDsignal'].values, decimals=3)
    if new_data.iloc[-1,]['MACD'] > new_data.iloc[-1,]['MACDsignal']:
        flag = '买入'
    else:
        flag = '卖出'
    line1 = (
        Line(init_opts=opts.InitOpts(width="800px", height="300px",theme=ThemeType.MACARONS))
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
            series_name="每日净值",
            y_axis=new_data['netWorth'].tolist(),
            label_opts=opts.LabelOpts(is_show=False, position="top", color="white"),
        )

            .set_global_opts(
            title_opts=opts.TitleOpts(title="{}：{}".format(code_name[code], flag), subtitle=code),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            # datazoom_opts=[opts.DataZoomOpts()],
        )
    )

    line2 = (
        Line(init_opts=opts.InitOpts(width="800px", height="300px", theme=ThemeType.MACARONS))
        .add_xaxis(xaxis_data=date)
        .add_yaxis(
            series_name="快线DIF",
            y_axis = new_data['MACD'].tolist(),
            label_opts=opts.LabelOpts(is_show=False, position="top", color="white"),
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[
            #         opts.MarkPointItem(type_="max", name="最大值"),
            #         opts.MarkPointItem(type_="min", name="最小值"),
            #     ]
            # ),
            # markline_opts=opts.MarkLineOpts(
            #     data=[opts.MarkLineItem(type_="average", name="平均值")]
            # ),
        )
        .add_yaxis(
            series_name="慢线DEA",
            y_axis=new_data['MACDsignal'],
            label_opts=opts.LabelOpts(is_show=False, position="top", color="white"),
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
            # ),
            # markline_opts=opts.MarkLineOpts(
            #     data=[
            #         opts.MarkLineItem(type_="average", name="平均值"),
            #         opts.MarkLineItem(symbol="none", x="90%", y="max"),
            #         opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
            #     ]
            # ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{}：{}".format(code_name[code], flag), subtitle=code),
            # datazoom_opts=[opts.DataZoomOpts()],
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            #legend_opts=opts.LegendOpts(pos_left="right"),
        )
        #.render("temperature_change_line_chart.html")
    )

    # 将上面定义好的图添加到 page
    page.add(
        line1,
        line2,
    )
    page.render("page_simple_layout.html")
    # # 最后的 Grid
    # grid_chart = Grid(init_opts=opts.InitOpts(width="1400px", height="800px"))
    #
    # grid_chart.add(
    #     line1,
    #     grid_opts=opts.GridOpts(
    #         pos_left="3%", pos_right="10%", pos_top="5%", height="35%"
    #     ),
    # )
    # grid_chart.add(
    #     line2,
    #     grid_opts=opts.GridOpts(
    #         pos_left="3%", pos_right="1%", pos_top="40%", height="35%"
    #     ),
    # )
    # grid_chart.render("data/{}.html".format(code_name[code]))
    # # os.system("data/{}.html".format(code_name[code]))
    # grid_chart.render_notebook()
