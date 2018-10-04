# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
Item 对象是种简单的容器，保存了爬取到得数据。
Item使用简单的class定义语法以及Field对象来声明。
"""


class DoubanItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()

    # 电影名称
    title = scrapy.Field()

    # 评分
    score = scrapy.Field()

    # 评论人数
    pople_num = scrapy.Field()

    # 导演
    director = scrapy.Field()

    # 年份
    year = scrapy.Field()

    # 地区
    area = scrapy.Field()

    # 类型
    clazz = scrapy.Field()

    # 一句话描述
    decsription = scrapy.Field()