#coding:utf-8

from lxml import etree
import requests
import sys
import re
import importlib

importlib.reload(sys)

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}


def spider(av):
    url = 'http://bilibili.com/video/av' + str(av)
    html = requests.get(url, headers=head)
    #print(html.text)
    selector = etree.HTML(html.text)
    content = selector.xpath("//html")
    
    for each in content:
        title = each.xpath('//div[@class="v-title"]/h1/@title')
        if title:
            cid_html_1 = each.xpath('//div[@class="scontent"]/iframe/@src')
            cid_html_2 = each.xpath('//div[@class="scontent"]/script/text()')
            
            if cid_html_1 or cid_html_2:
                if cid_html_1:
                    cid_html = cid_html_1[0]
                    #print('cid_html_1: '+cid_html_1[0])
                else:
                    cid_html = cid_html_2[0]
                    #print('cid_html_2: '+cid_html_2[0])		#format: EmbedPlayer('player', "//static.hdslb.com/play.swf", "cid=6154070&aid=3830668&pre_ad=0");

                cids = re.findall(r'cid=.+&aid', cid_html)
                cid = cids[0].replace("cid=", "").replace("&aid", "")
                comment_url = 'http://comment.bilibili.com/' + str(cid) + '.xml'
                #print(comment_url)		format: http://comment.bilibili.com/6154070.xml
                comment_text = requests.get(comment_url, headers=head)
                comment_selector = etree.HTML(comment_text.content)
                comment_content = comment_selector.xpath('//i')
                for comment_each in comment_content:
                    comments = comment_each.xpath('//d/text()')
                    if comments:
                        for comment in comments:
                        	f.writelines(comment + '\n')
                        	pass
            else:
                print('error')
        else:
            print('video not found!')

if __name__ == '__main__':
    av = input('input av:')
    #av = '3830668'
    f = open(av + '.txt', 'w', encoding='utf-8')
    spider(av)
