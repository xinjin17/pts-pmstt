import os
import subprocess
import shutil


class new_ts_mp4(object):

    def __init__(self, whole):
        self.whole = whole
        self.whole_0 = whole[0]
        self.start = whole[0] + "\\*.ts"
        self.end_ts = whole[0] + "\\new.ts"
        self.end = whole[1] + '\\' + whole[2] + '.mp4'

        # 合并.ts为一个大文件函数的调用
        self.new_ts()
        # 把m3u8转换成mp4
        self.new_mp4()


    # 合成新的全部ts数据
    def new_ts(self):
        command = f'copy/b {self.start} {self.end_ts}'

        print(f'启动ffmpeg,命令')
        # 通过subprocess调用系统命令行
        subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
        if os.path.exists(self.end_ts):
            for filename in os.listdir(self.whole_0):
                if os.path.exists(self.end_ts):
                    pass
                else:
                    try:
                        os.remove(filename)
                        print(f"文件 {filename} 已被成功删除！")
                    except OSError as e:
                        print(f"删除文件时出错: {e.strerror}")
        else:
            new_ts_mp4(self.whole).new_ts()

        print("new.ts完成")

    # 把全部ts数据合成mp4数据
    def new_mp4(self):
        command = f'ffmpeg -i {self.end_ts} -acodec copy -vcodec copy -f mp4 {self.end}'

        print(f'启动ffmpeg,命令')
        # 通过subprocess调用系统命令行
        subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
        if os.path.exists(self.end):
            # 删除文件夹
            if os.path.exists(self.whole_0):
                shutil.rmtree(self.whole_0)
            else:
                print("文件夹不存在.")
        else:
            new_ts_mp4(self.whole).new_mp4()
        print("new.mp4完成")


def main(whole):
    new_ts_mp4(whole)
    

