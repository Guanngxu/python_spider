#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : weixin_gzh.py
# @Author: 刘绪光
# @Date  : 2018/9/29
# @Desc  : 微信公众号爬虫

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


DRIVER_PATH = "你的 chromedriver 路径"
USERNAME = "你的账号"
PASSWORD = "你的密码"
OFFICIAL_ACCOUNT = "你想爬的公众号名称"
BASE_URL = "https://mp.weixin.qq.com/"


class WXSpider:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    def __open_gzh(self):
        self.driver.get(BASE_URL)
        self.driver.maximize_window()
        username_element = self.driver.find_element_by_name("account")
        password_element = self.driver.find_element_by_name("password")
        login_btn = self.driver.find_element_by_class_name("btn_login")
        username_element.send_keys(USERNAME)
        password_element.send_keys(PASSWORD)
        login_btn.click()
        WebDriverWait(driver=self.driver, timeout=200).until(
            ec.url_contains("cgi-bin/home?t=home/index")
        )
        # 一定要设置这一步，不然公众平台菜单栏不会自动展开
        self.driver.maximize_window()

    def __open_write_page(self):
        management = self.driver.find_element_by_class_name("weui-desktop-menu_management")
        material_manage = management.find_element_by_css_selector("a[title='素材管理']")
        material_manage.click()
        new_material = self.driver.find_element_by_class_name("weui-desktop-btn_main")
        new_material.click()
        # 关闭公众平台首页
        handles = self.driver.window_handles
        self.driver.close()
        self.driver.switch_to_window(handles[1])

    def __open_official_list(self):
        # 超链接
        link_click = self.driver.find_element_by_class_name("edui-for-link")
        link_click.click()
        time.sleep(3)
        # 查找文章
        radio = self.driver.find_element_by_class_name("frm_vertical_lh").find_elements_by_tag_name("label")[1]
        radio.click()
        # 输入查找关键字
        search_input = self.driver.find_element_by_class_name("js_acc_search_input")
        search_input.send_keys(OFFICIAL_ACCOUNT)
        search_btn = self.driver.find_element_by_class_name("js_acc_search_btn")
        search_btn.click()
        # 等待5秒，待公众号列表加载完毕
        time.sleep(5)
        result_list = self.driver.find_element_by_class_name("js_acc_list").find_elements_by_tag_name("div")
        result_list[0].click()

    def __get_article_list(self):
    # 等待文章列表加载
    time.sleep(5)
    total_page = self.driver.find_element_by_class_name("search_article_result")\
        .find_element_by_class_name("js_article_pagebar").find_element_by_class_name("page_nav_area")\
        .find_element_by_class_name("page_num")\
        .find_elements_by_tag_name("label")[1].text
    total_page = int(total_page)
    articles = []
    try:
        for i in range(0, total_page-1):
            time.sleep(5)
            next_page = self.driver.find_element_by_class_name("search_article_result")\
                .find_element_by_class_name("js_article_pagebar").find_element_by_class_name("pagination")\
                .find_element_by_class_name("page_nav_area").find_element_by_class_name("page_next")
            article_list = self.driver.find_element_by_class_name("js_article_list")\
                .find_element_by_class_name(" my_link_list").find_elements_by_tag_name("li")
            for article in article_list:
                article_info = {
                    "date": article.find_element_by_class_name("date").text,
                    "title": article.find_element_by_tag_name("a").text,
                    "link": article.find_element_by_tag_name("a").get_attribute("href")
                    }
                articles.append(article_info)
            next_page.click()
        return articles
    except Exception as e:
        print(articles)
        print(e)
        print("当前页面" + str(i))
        return articles

    def crawl_gzh(self):
        self.__open_gzh()
        self.__open_write_page()
        self.__open_official_list()
        result = self.__get_article_list()
        self.driver.close()
        return result


if __name__ == '__main__':
    wx_spider = WXSpider()
    articles = wx_spider.crawl_gzh()
    print(articles)
