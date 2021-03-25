# filename: sorter.py
import argparse 
import os
import shutil
import re

class Picture:
    # 建構式
    def __init__(self, path):
        self.path = path
        self.name = path.split("\\")[-1].strip(".jpg")
        # name rule : title_tag1#tag2-num.jpg
        self.title = ""
        self.tag1 = ""
        self.tag2 = ""
        self.num = ""
        self.parse()
    # 方法(Method)
    def naming(self):
        i = 0
        while i < 100:
            try:
                serial_num = self.num + i
                re_name = self.title+self.tag1+self.tag2+"-"+str(serial_num)+".jpg"
                os.rename(self.path,self.path[:self.path.index(self.name)]+re_name)
                break
            except:
                i = i + 1
    def parse(self):
        self.title = re.findall(r"^[A-Za-z]+\-?[A-Za-z]+",self.name)[0]
        properties = re.findall(r"[\-_#\s][A-Za-z0-9]+",self.name)
        for prop in properties:
            if( len(re.findall(r"[\s\-_][0-9]+",prop))):
                self.num = int(re.sub(r"[\s\-_]", "", prop))
            elif(prop.find("_") != -1):
                self.tag1 = prop
            elif(prop.find("#") != -1):
                self.tag2 = prop

class Directory:
    # 建構式
    def __init__(self, path):
        if path == "" or path is None:
            return
        if(os.path.isdir(path) is False):
            os.makedirs(path)
        self.path = path 
        self.name = path.split("\\")[-1]
        self.contain = os.listdir(self.path)
        self.size = self.contain.__len__()
    # 方法(Method)
    def ls(self):
        return self.contain
    def rename(self,re_name):
        os.rename(self.path,self.path[:self.path.index(self.name)]+re_name)
        self.name = re_name

    def sort(self,sorter):
        for file in self.contain:
            if os.path.isdir("{}\\{}".format(self.path,file)) :
                continue
            pic = Picture("{}\\{}".format(self.path,file))
            if(sorter == "title"):
                dir_name = pic.title
            elif(sorter == "tag1"):
                dir_name = pic.tag1.lstrip('_')
            elif(sorter == "tag2"):
                dir_name = pic.tag2.lstrip('#')
            if not os.path.isdir("{}\\{}".format(self.path,dir_name)):
                os.mkdir("{}\\{}".format(self.path,dir_name))
            try:
                shutil.move("{}\\{}".format(self.path,file),"{}\\{}".format(self.path,dir_name))
            except:
                print("unsorted",pic.path)
    def fetch(self):
        for folder in self.contain:
            if os.path.isdir("{}\\{}".format(self.path,folder)) :
                sub_dir = Directory("{}\\{}".format(self.path,folder))
                for file in sub_dir.contain:
                    shutil.move("{}\\{}".format(sub_dir.path,file),self.path)
                os.rmdir(sub_dir.path)
    def calculate_len(self):
        for folder in self.contain:
            if os.path.isdir("{}\\{}".format(self.path,folder)) :
                sub_dir = Directory("{}\\{}".format(self.path,folder))
                if(folder.find("[") != -1 and folder.find("]") != -1):
                    sub_dir.rename(re.sub(r'\[\d+\]', "[{}]".format(sub_dir.size), folder))
                else:
                    sub_dir.rename("{}[{}]".format(folder,sub_dir.size))
    def addAttr(self,Attr,pos):
        for file in self.contain:
            if os.path.isfile("{}\\{}".format(self.path,file)) :
                pic = Picture("{}\\{}".format(self.path,file))
                if(pos == "tag1"):
                    pic.tag1 = "_"+Attr
                elif(pos == "tag2"):
                    pic.tag2 = "#"+Attr
                pic.naming()
    def rmAttr(self,pos):
        for file in self.contain:
            if os.path.isfile("{}\\{}".format(self.path,file)) :
                pic = Picture("{}\\{}".format(self.path,file))
                if(pos == "tag1"):
                    pic.tag1 = ""
                elif(pos == "tag2"):
                    pic.tag2 = ""
                pic.naming()

def process_command():
    parser = argparse.ArgumentParser(description='This is file sorter. name rule : title_tag1-num#tag2.jpg')
    parser.add_argument('path', type=str, help='selected folder to operate')
    parser.add_argument("-s",'--sort', type=str, choices=["title","tag1","tag2"],metavar='tag1',help='Sort files into directories by specific tag. (title,tag1,tag2)')
    parser.add_argument("-f",'--fetch',action="store_true", help='Fetch files from all directories.')
    parser.add_argument("-a",'--add', nargs=2 ,metavar=('str', 'tag'),type=str,help='Add string to all of files in directories. (tag1,tag2)')
    parser.add_argument("-r",'--remove', choices=["tag1","tag2"],metavar='tag',type=str,help='Remove string to all of files in directories. (tag1,tag2)')
    parser.add_argument("-l",'--len',action="store_true", help='Calculate the number of files and name the number at the end of the folder')

    return parser.parse_args()

if __name__ == '__main__':
    args = process_command()
    target = Directory(args.path)
    if(args.add):
        if not (args.add[1] in ["tag1","tag2"]):
            print("Invalid tag1. please use (tag1,tag2) and try it again!")
            quit()
        target.addAttr(args.add[0],args.add[1])
    elif(args.remove):
        if not (args.remove in ["tag1","tag2"]):
            print("Invalid tag1. please use (tag1,tag2) and try it again!")
            quit()
        target.rmAttr(args.remove)
    if (args.sort):
        target.sort(args.sort)
    elif(args.fetch):
        target.fetch()
    if(args.len):
        target.calculate_len()
    print("Mission complete")
    

