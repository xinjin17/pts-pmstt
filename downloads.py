import time
from urllib.parse import urljoin
import re
import requests
import os
from Cryptodome.Cipher import AES


class download(object):

    def __init__(self, url, lists):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        }

        # 网站
        self.url = url

        # 切片
        self.url_os = self.url.rsplit('/')[-2]


        if lists == 0:
            self.lists = 0
        else:
            self.lists = lists

    def download_m3u8(self) -> list:

        # 获取一级
        reqs = requests.get(url=self.url, headers=self.headers).text
        # 去除最后的两个回车
        reqs_text = reqs.strip()
        # reqs_text = reqs_text.strip()

        reqs_text_url = ''
        key = ""
        iv = ""
        if len(reqs_text.split('\n')) <= 6:
            # 获取二级地址
            for line in reqs_text.split('\n'):
                if not line.startswith('#'):
                    reqs_text_url = line
                    # 将开始和获取的不同之处合并
                    reqs_text_url = urljoin(self.url, reqs_text_url)

            reqs_new = requests.get(url=reqs_text_url, headers=self.headers).text
            # 去除最后的两个回车
            reqs_text = reqs_new.strip()

        # key和iv的密钥
        key = b""
        iv = b"0000000000000000"
        try:
            # 解析出秘钥key
            key_url = re.findall('URI="(.*?)"', reqs_text, re.S)[0]
            key_url = urljoin(self.url, key_url)
            # 解析出秘钥key和iv地址
            key = requests.get(url=key_url, headers=self.headers).content
        except Exception as e:
            print(e)
        finally:
            pass

        if len(reqs_text_url) > 0:
            self.url = reqs_text_url

        # 创建文件夹
        if not os.path.exists(self.url_os):
            os.mkdir(self.url_os)

        # 存放ts的链接
        ts_urls_list = []
        lists = self.lists

        # 获取每一个ts的地址
        for line in reqs_text.split('\n'):
            if not line.startswith('#'):
                ts_url = line
                # 链接完整的路径
                ts_urls = urljoin(self.url, ts_url)
                ts_urls_list.append(ts_urls)
        # 减少数据对系统调用，第一次进行时要使用这是模块，当数据出现错误是就不在使用这个模块
        if lists == 0:
            # 获取文件夹中有多少个文件
            file_count = 0
            for filename in os.listdir(self.url_os):
                if os.path.isfile(os.path.join(self.url_os, filename)):
                    file_count += 1
            # 当用户没有一次性完成下载的时候，在一次下载是不再从头开始下载和判断当这个下载完成是否已经完成全部下载完直接跳到下一步
            if len(ts_urls_list) > file_count:
                lists = file_count
            else:
                lists = len(ts_urls_list)
                print(lists)

        # 当在下载的过程中出现错误是不再从新下载已经下载好的
        ts_urls_list = ts_urls_list[lists:]
        print(len(ts_urls_list))


        ips = 1
        ipts = 10000
        # 请求每一个ts的地址
        try:
            for url in ts_urls_list:
                ts_data = requests.get(url=url, headers=self.headers).content
                # 判断key是否存在
                if key != b"":
                    # 密钥解密
                    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
                    ts_data = aes.decrypt(ts_data)
                ts_mane = url.split('/')[-1]
                ts_path = self.url_os + '/' + str(ips + ipts) + '.ts'
                with open(ts_path, 'wb') as fp:
                    # time.sleep(3)
                    fp.write(ts_data)
                    print(ts_mane + ',' + str(ips) + '个/' + str(len(ts_urls_list)) + '个,完成')
                    ips = ips + 1
        except Exception as e:
            print(e)
        finally:
            time.sleep(4)
            # print("在来")


        # 返回原始列表的长度和最后下载的长度
        return [len(ts_urls_list), (lists + ips - 1)]


def main(url):
    # url = input("网站的m3u8：")
    lists = 0
    # 检查下载的数据数量是否完全下载完成，没有完成再调一次函数
    while lists >= 0:
        # print(lists)
        download_url = download(url, lists)
        end_list = download_url.download_m3u8()
        # 判断是否在下载的过程是否出现错误，当出现错误在回调在下载
        if end_list[0] > end_list[1]:
            lists = end_list[1]
            print(lists)
        else:
            break
    print("ok")



