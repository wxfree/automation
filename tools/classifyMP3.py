import shutil
from mutagen import File
import os
# os.mkdir(root_dir + '/文件夹名')正反斜杠好像都行

root_dir = r'C:\Users\Administrator\Desktop\music'
root_dir_bak = r'C:\Users\Administrator\Desktop\musicbak'
# 切换到根目录
os.chdir(root_dir)
# 备份源数据
shutil.copytree(root_dir, root_dir_bak)
# 获取数据
for item in os.listdir():
    # item是文件名或者文件夹名
    # 组装所有文件、文件夹的路径
    path = os.path.join(root_dir, item)
    # 判断是否是文件，将文件夹过滤，下面的path就是歌曲的完整字符串路径
    if os.path.isfile(path):
        # 使用mutagen获取mp3歌手、专辑、歌名信息，专辑信息暂时也没啥用，分类完成后再次根据专辑名细分(暂时无用)
        # {'TIT2': TIT2(encoding=<Encoding.UTF8: 3>, text=['你的微笑']), 'TPE1': TPE1(encoding=<Encoding.UTF8: 3>, text=['F.I.R.飞儿乐团']), 'TALB': TALB(encoding=<Encoding.UTF8: 3>, text=['F.I.R.飞儿乐团'])}
        targetFile = File(path)
        author = targetFile['TPE1'].text[0]
        title = targetFile['TIT2'].text[0]
        album = targetFile['TALB'].text[0]
        # 确保数据存在，否则可能出问题(此处需要找几个得不到信息的mp3试试)
        if author and title and album:
            # 拼接歌手名作为文件夹
            targetPath = root_dir + '\\' + author
            if os.path.exists(targetPath):
                # 存在这个文件夹就直接把mp3文件移动到这个文件夹下
                shutil.move(path, targetPath)
            else:
                # 否则就先创建这个文件夹，再移动
                os.mkdir(targetPath)
                shutil.move(path, targetPath)

# 将分类好的mp3文件全部丢到一个文件夹下,上面代码的逆操作
# for root, dirs, files in os.walk(root_dir):
#     print(root)
#     if len(files) > 0:
#         for file in files:
#             print(file)
#             shutil.move(root + '\\' + file, root_dir)
