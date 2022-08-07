import shutil
from mutagen import File
import os
from automation.common.log_service import LogService
import datetime
import traceback
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
log = LogService(__name__).log()
# os.mkdir(root_dir + '/文件夹名')正反斜杠好像都行
# 备份之前要考虑备份文件夹是否存在，如果不存在直接复制黏贴，如果存在就要研究如何删掉这个文件夹os.remove, os.rmdir
# 使用time模块创建备份文件夹精确到秒就不会出现重复备份文件夹问题了，和谐解决上面的问题


class ClassifyMp3:
    def __init__(self, root_path, need_backup=False):
        """
            :param root_path: MP3所在路径,绝对路径
            :param need_backup: 是否需要备份
        """
        self.rootPath = root_path
        # 备份数据
        if need_backup:
            self.backup()
        # 切换到根目录
        os.chdir(self.rootPath)

    def backup(self):
        """不放心可以先备份rootPath文件夹"""
        now = datetime.datetime.now()
        str_time = now.strftime('%Y%m%d%H%M%S')
        backup_dir = self.rootPath + '备份' + str_time
        # copytree方法目标路径(backup_dir)不能存在
        shutil.copytree(self.rootPath, backup_dir)

    def move_file_into_folder(self):
        """将当前rootPath下的mp3文件移动到相应歌手的文件夹下"""
        for item in os.listdir():
            try:
                # mac会有很多.DS_Store文件
                if item == '.DS_Store':
                    continue
                music_path = os.path.join(self.rootPath, item)
                if os.path.isfile(music_path):
                    # 使用mutagen获取mp3歌手、专辑、歌名信息，专辑信息暂时也没啥用，分类完成后再次根据专辑名细分(暂时无用)
                    target_file = File(music_path)
                    if not target_file:
                        log.error(f"line-45:{music_path}:不存在歌曲信息字段")
                        continue
                    author = target_file['TPE1'].text[0]
                    title = target_file['TIT2'].text[0]
                    album = target_file['TALB'].text[0]
                    if author and title and album:
                        # 拼接歌手名作为文件夹
                        target_path = self.rootPath + '/' + author
                        log.info(f"{target_path}")
                        if os.path.exists(target_path):
                            # 存在这个文件夹就直接把mp3文件移动到这个文件夹下
                            shutil.move(music_path, target_path)
                        else:
                            # 否则就先创建这个文件夹，再移动
                            os.mkdir(target_path)
                            # 如果目标文件夹中已经有了该曲目咋办,try里可以弄到
                            shutil.move(music_path, target_path)
                        log.info(f"{item} 分类成功")
            except KeyError:
                log.info(f"{item} 音乐信息不完善")
                # log.error(f"{traceback.format_exc()}")
                continue
            except FileNotFoundError:
                log.info(f"{item} 音乐信息不完善")
                log.error(f"{traceback.format_exc()}")
                continue 
            except shutil.Error:
                log.error(f"{traceback.format_exc()}")
                continue 

    def move_file_out_folder(self):
        """将rootPath下的各种mp3文件移动到rootPath下,要保证第一层文件夹下没有mp3文件"""
        for root, dirs, files in os.walk(self.rootPath):
            try:
                log.info(files)
                if len(files) > 0:
                    for file in files:
                        # 只关心MP3文件
                        if file != '.DS_Store' and file.endswith('.mp3'):
                            log.info(file)
                            shutil.move(root + '/' + file, self.rootPath)
            except shutil.Error:
                log.error(f"{traceback.format_exc}")
                continue


    @classmethod
    def set_mp3_info(cls, path, title, author, album):
        """有些mp3没有歌手、专辑、歌名信息,就手动输入下"""
        music = ID3(path)
        music.add(TIT2(encoding=3, text=title))  # 插入歌名
        music.add(TPE1(encoding=3, text=author))  # 插入作者
        music.add(TALB(encoding=3, text=album))
        music.save()
        log.info(File(path))


root_dir = r'/Users/wangxin/Downloads/music'
mp3 = ClassifyMp3(root_dir)
# 把所有文件夹中的音乐挪到外层
mp3.move_file_out_folder()
# 把所有音乐按歌手名建文件夹并分类
# mp3.move_file_into_folder()
# 根据音乐地址,修改音乐的歌名、作者、专辑
# mp3.set_mp3_info('/Users/wangxin/Downloads/music/情歌.mp3', '情歌', '梁静茹', '静茹&情歌-别再为他流泪')
# ClassifyMp3.set_mp3_info('/Users/wangxin/Downloads/music/honey.mp3', 'honey', '王心凌', 'Honey')
