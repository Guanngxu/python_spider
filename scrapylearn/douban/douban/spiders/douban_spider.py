#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : douban_spider.py
# @Author: 刘绪光
# @Date  : 2018/6/9
# @Desc  :

from scrapy.spider import Spider
from douban.items import DoubanItem
from scrapy import Request
from bs4 import BeautifulSoup
import time



class douban_spider(Spider):

    count = 1

    # 爬虫启动命令
    name = 'douban'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    # 处理爬取的数据
    def parse(self, response):

        print('第', self.count, '页')
        self.count += 1

        item = DoubanItem()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 选出电影列表
        movies = soup.select('#content div div.article ol li')

        for movie in movies:
            item['title'] = movie.select('.title')[0].text
            item['ranking'] = movie.select('em')[0].text
            item['score'] = movie.select('.rating_num')[0].text
            item['pople_num'] = movie.select('.star span')[3].text

            # 包含导演、年份、地区、类别
            info = movie.select('.bd p')[0].text
            director = info.strip().split('\n')[0].split('   ')
            yac = info.strip().split('\n')[1].strip().split(' / ')

            item['director'] = director[0].split(': ')[1]
            item['year'] = yac[0]
            item['area'] = yac[1]
            item['clazz'] = yac[2]

            if len(movie.select('.inq')) is not 0:
                item['decsription'] = movie.select('.inq')[0].text
            else:
                item['decsription'] = 'None'
            yield item

        next_url = soup.select('.paginator .next a')[0]['href']
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url
            yield Request(next_url, headers=self.headers)
