import time
from os import path
import os
log = path.join(path.abspath(r"C:\Users\kenne\OneDrive\Kode\Python\Folder Organiser\data"),"prev_log")
"""
os.mkdir()
os.listdir()
shutil.move()
shutil.rmtree()
path.join()
path.exists()
path.isdir()
path.isfile()
path.splitext()
"""

class folderOrganizer:
    
    def __init__(self,basedir,folder_names,folders):
        self.basedir = path.abspath(basedir)
        self.folder_names = folder_names
        self.folders = folders
        self.current_folder = None
        self.file_list = None
        self.setup_flag = None
        self.getList()

    def setupFolders(self,*additional_folders):
        if not self.setup_flag:
            for dir in self.folders: 
                folder_path = path.join(self.basedir,dir)
                if not path.exists(folder_path): # Lag mappen om den ikke eksisterer
                    print("Making directory: ",folder_path)
                    os.mkdir(folder_path)
                else:
                    pass

                data = {
                    "extensions": self.folders[dir], #relevante filtyper for mappen
                    "folder": dir #Nåværende mappe
                    } 
                self.getFiles(data)
            self.setup_flag = True
            self.miscSort()
        else:
            for dir in additional_folders:
                misc_path = path.join(self.basedir,"misc_files")
                folder_path = path.join(misc_path,dir)
                if path.exists(folder_path):
                    print("exists")
                else:
                    os.mkdir(folder_path)


    def getList(self):
        all_files = os.listdir(self.basedir)
        self.file_list = all_files
        with open(file=log,mode="w") as logfile:
            for line in all_files:
                logfile.write(line + " ")


        return all_files

    def getFiles(self,data):
        extensions = data["extensions"]
        self.current_folder = data["folder"] 
        relevantFiles: list = []

        if not relevantFiles:
            for file in self.file_list: # Itererer over listen 
                current_extension = self.getExt(file)
                try:
                    if not current_extension.lower() in extensions: 
                        continue
                    else: 
                        print(file)
                        relevantFiles.append(file) # Hvis filen matcher filtypen som skal i mappen
                except TypeError:
                    continue
        else: 
            pass
        self.moveFiles(relevantFiles) # gir fra seg alle relevante filer

    def getExt(self,file): # returnerer filtype fra fil
        extension = path.splitext(file)[1]
        return extension

    def moveFiles(self,files):
        import shutil
        for file in files:
            target = path.join(self.basedir,self.current_folder)
            source = path.join(self.basedir,file)
            if not path.exists(target):
                pass
            else:
                name,ext = path.splitext(file)
                new_source = path.join(self.basedir,name+"1"+ext)
                os.rename(source,new_source)
                source = new_source
            try:

                shutil.move(source,target)
            except Exception as e:
                continue
        return

    def miscSort(self):
        import shutil
        misc = ["misc_folders","misc_files"]
        self.getList()
        for File in self.file_list:
            source = path.join(self.basedir,File)
            if path.isdir(source):
                if File not in self.folders.keys() and File not in misc:
                    target_folder = path.join(self.basedir,misc[0])
                    try:
                        shutil.move(source,target_folder)
                    except Exception as e:
                        print(e)
                        continue

            elif path.isfile(source) and File not in self.folders:
                extension = path.splitext(File)[1]
                if len(extension) < 1:
                    extension = "no_extension"
                self.setupFolders(extension)
                target_folder = path.join(self.basedir,misc[1],extension)
                try:
                    shutil.move(source,target_folder)
                except Exception as e:
                    print(e)
                    continue
     