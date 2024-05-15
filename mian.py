import os
from downloads import main as downloads
from new_ts import main as new_ts



def mian():
    # 获取网站的m3u8类 download类
    url = input("网站的m3u8：")
    url_os = url.rsplit('/')[-2]

    # 修改视频格式
    whole = []
    # 文件的路径在download类中决定的
    end = input('保存文件的路径：')
    mane = input('保存文件的路径的名字:')
    whole.append(url_os)
    whole.append(end)
    whole.append(mane)
    download = downloads(url)
    new_list = new_ts(whole)



if __name__ == '__main__':
    mian()



