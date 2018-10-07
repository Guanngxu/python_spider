#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : html_to_pdf.py
# @Author: 刘绪光
# @Date  : 2018/10/5
# @Desc  : 将 html 网页截屏并生成 pdf 文件


import os
import time
from fpdf import FPDF
from selenium import webdriver

PHANTOMJS_PATH = "D:/workspace/tools/chromedriver/phantomjs.exe"
PATH = "articleimgs/"


def screen_shot(article_list):
    br = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
    br.maximize_window()
    for article in article_list:
        br.get(article.get("link"))
        time.sleep(3)
        js = "window.scrollTo(0,document.body.scrollHeight)"
        br.execute_script(js)
        time.sleep(3)
        br.save_screenshot(PATH + article.get("title") + ".png")
    br.close()
    print("screenshot finishied")


def imgs_to_pdf():
    index = 0
    pdf = FPDF()
    pdf.set_creator("刘小绪同学")
    pdf.set_author("刘小绪同学")
    pdf.add_page()
    for img in os.listdir(PATH):
        print(index)
        index += 1
        pdf.image(PATH+img, w=190, h=280)
    pdf.output("articles.pdf")


if __name__ == '__main__':
    imgs_to_pdf()
