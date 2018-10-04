#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : hello_spider.py
# @Author: 刘绪光
# @Date  : 2018/6/9
# @Desc  :
from scrapy.spider import Spider


class BlogSpider(Spider):

    # 爬虫启动命令
    name = 'hello_world'

    # Spider在启动时进行爬取的url列表
    start_urls = ['https://woodenrobot.me']


    def parse(self, response):
        """
        每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数
        该方法负责解析返回的数据(response data)
        提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象
        """
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            print(title.strip())