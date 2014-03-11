#!/usr/bin/python
#coding:utf-8
import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

root_path = os.path.dirname(__file__)
watch_path = os.path.join(root_path, 'source')
#创建子进程并自动执行编译程序

re_all = r"/\w+\.(js|css|less)$"
re_js = r"/\w+\.js$"
re_css = r"/\w+\.css$"
re_less = r"/\w+\.less$"

def mkdirs(path):
    path = path.strip()
    path = re.sub(r'/[^/]*\.\w+$','/',path)
    path = path.strip().rstrip('/')
    if not os.path.exists(path):
        print "Create path: "+path
        os.makedirs(path)

def compile_files(src,dest):
    if re.search(re_js, src):
        cmd = "uglifyjs %s -o %s"%(src, dest)
        print cmd
        os.system(cmd)
    elif re.search(re_css, src):
        cmd = "sqwish %s -o %s"%(src, dest)
        print cmd
        os.system(cmd)
    elif re.search(re_less, src):
        dest = re.sub(r'less$', 'css', dest)
        cmd = "lessc -x %s %s"%(src, dest)
        print cmd
        os.system(cmd)
    else:
        cmd = "cp %s %s"%(src, dest)

def get_file_list(path):
    result = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename != ".DS_Store":
                result.append(dirpath+'/'+filename)
    return result

class FileHandler(FileSystemEventHandler):
    def _get_filename(self,path):
        result = re.search(re_all, path)
        if not result:
            print "Don't surpport file: "+path
            return False
        else:
            return result.group(0).lstrip('/')

    def on_created(self, event):
        if not event.is_directory:
            path = event.src_path
            file_name = self._get_filename(path)
            if file_name:
                src_dir_path = path.rstrip(file_name)
                dest_dir_path = re.sub(r'/source/','/static/',src_dir_path)
                mkdirs(dest_dir_path)
                dest_path = re.sub(r'/source/','/static/',path)
                compile_files(path,dest_path)

    def on_modified(self, event):
        if not event.is_directory:
            path = event.src_path
            file_name = self._get_filename(path)
            if file_name:
                src_dir_path = path.rstrip(file_name)
                dest_dir_path = re.sub(r'/source/','/static/',src_dir_path)
                mkdirs(dest_dir_path)
                dest_path = re.sub(r'/source/','/static/',path)
                compile_files(path,dest_path)

    def on_deleted(self, event):
        pass

    def on_moved(self, event):
        if not event.is_directory:
            pass

def run_child():
    #first run should compile every file
    lists = get_file_list(watch_path)
    for src_path in lists:
        dest_path = re.sub(r'/source/','/static/',src_path)
        mkdirs(dest_path)
        if not os.path.isfile(dest_path):
            compile_files(src_path, dest_path)

    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    observer.start()
 
    try:
        print "Started File Watch At : "+watch_path
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def run():
    cmd = "dev_appserver.py . --storage_path=~/tmp/gae/storage"
    os.system(cmd)

try:
    pid = os.fork()
    #child process
    if pid == 0:
        run_child()
    else:
        run()
except Exception,e:
    print "自动编译进程错误"
    print e


