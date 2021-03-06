#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
创立一个timeline
template: https://bootsnipp.com/snippets/featured/timeline-21-with-images-and-responsive
"""
import os
import sys
from template import *
from utilities import reformat_time

class timecard:

    def __init__(self):
        self.time = [] # each: '2018-1-2'
        self.meta = [] # each: {'up_num','retweet_num','comment_num'}
        self.content = [] # each: 'ransfdlsmdkglja'
        self.img_path = [] # each: '/path/to/img.jpg'
        self.img_src = [] # each: 'url-to-jpg'

    def load_text(self, inputfile):
        print("为timecard加载文字信息")
        if not os.path.isfile(inputfile):
            print("文字文件不存在 %s\n加载失败" % inputfile)
            return

        from utilities import read_weibo_file
        weibo = read_weibo_file(inputfile)
        self.time = weibo['publish_time']
        self.content = weibo['content']
        self.meta = weibo['meta']
        self.img_src = [""] * len(self.content)
        self.img_path = [""] * len(self.content)

        for i in range(0, len(self.time)): # change Y-m-d H:M to YmdHM
            self.time[i] = reformat_time(self.time[i])

    def load_imgsrc(self, imgfile):
        print("为timecard加载图片超链接")
        if not os.path.isfile(imgfile):
            print("图片文件不存在 %s\n加载失败" % imgfile)
            return

        with open(imgfile,'r') as f:
            for line in f:
                weibo_title = int(line.split(',')[0])
                imgurl = line.split(',')[1]

                # 使用第一张有效图片链接
                if self.img_src[weibo_title - 1] == "" and len(imgurl.split('.'))>1:
                    self.img_src[weibo_title - 1] = imgurl.strip()

    def load_imgsrc_local(self, img_dir):
        print("为timecard加载图片超链接")
        if not os.path.isdir(img_dir):
            print("文件夹不存在 %s" % img_dir)
            return

        from utilities import get_subdir
        from config import image_format

        dirs = get_subdir(img_dir)
        for each_dir in dirs:
            files = [os.path.join(each_dir,f) for f in os.listdir(each_dir)
                     if os.path.isfile(os.path.join(each_dir,f))]
            files = [f for f in files if f.split('.')[-1] in image_format]
            if files:
                weibo_title = int(each_dir.split(os.path.sep)[-2])
                self.img_path[weibo_title - 1] = files[0]

    def print_cards(self):
        for i in range(0, len(self.time)):
            weibo = (self.time[i] + ': ' + self.content[i] + '\n' + 'up: %d  retweet: %d  comment: %d'
                             % (self.meta[i]['up_num'], self.meta[i]['retweet_num'], self.meta[i]['comment_num']))
            print(weibo + '\n')

        print("Total: %d" % len(self.time))

def template_wrapper(timecards, template_name, ignore_retweet=True):
    """ wrapper function to apply timeline tempalte to timecards
    """
    template_path = os.getcwd() + os.path.sep + "timeline_templates" + os.path.sep + template_name

    header_file = template_path + os.path.sep + "head.html"
    tail_file = template_path + os.path.sep + "tail.html"

    if not os.path.isfile(header_file) or not os.path.isfile(tail_file):
        print("HTML template incomplete.")
        sys.exit()

    with open(header_file, 'rt', encoding='utf-8') as hf:
        header_string = ''.join(hf.readlines())

    with open(tail_file, 'rt', encoding='utf-8') as tf:
        tail_string = ''.join(tf.readlines())

    # build body
    body_string = ""
    if template_name == "PinkElegance":
        body_string = tempalte_PinkElegance(timecards, ignore_retweet)
    elif template_name == "FlexBox":
        body_string = template_FlexBox(timecards, ignore_retweet)
    elif template_name == "PinkStar":
        body_string = template_PinkStar(timecards,"https://weibo.com/u/5491331848", ignore_retweet)

    html_content = header_string + body_string + tail_string

    with open(template_path + os.path.sep + "mytimeline.html", 'wt', encoding='utf-8') as f:
        f.write(html_content)

def build_timeline(user_id, template_name="PinkElegance"):
    """ source_path = os.getcwd() + '/weibo/weibo_id/'
    """

    # weibo_path
    weibo_path = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(user_id)
    if not os.path.isdir(weibo_path):
        print("No weibo path")
        sys.exit()

    # build timecards
    timecards = timecard()
    timecards.load_text(weibo_path + os.path.sep + str(user_id) + '.txt')
    timecards.load_imgsrc(weibo_path + os.path.sep + "img_list.txt")

    # filter
    ignore_retweet = True

    # choose template
    template_wrapper(timecards, template_name, ignore_retweet)
