from module.Organizer import folderOrganizer
print("hey")
class DownloadOrganize:
    folder_names = ["docs","compressed","installers","executables","pictues"]


    folders = {
        "docs": 
            [".pdf",".doc",".docx",".txt",".xlsx",".xls",".rtf",".pptx"],
        "compressed": 
            [".zip", ".rar", ".7z", ".gz", ".tar",".tgz",".cab"],
        "installers":
            [".msi"],
        "executables": 
            [".exe", ".bat",".jar",".ps1"],
        "pictures":
            [".png",".bmp",".jpeg",".jpg"],
        "video":
            [".mp4",".avi"],
        "audio":
            [".mp3"],
        "image":
            [".img",".iso",".cso"],
        "android_apps":
            [".apk",".xapk"],
        "platform_extensions":
            [".whl",".vsix",".vbox-extpack"],
        "misc_files":
            None
        }

    def hasChanged(self):
        from os import path
        import os
        import sys
        current_items = self.setup().getList()
        log = path.join(path.abspath(r"C:\Users\kenne\OneDrive\Kode\Python\Folder Organiser\data"),"log")
        log_content = None
        with open(file=log, mode="r", encoding="utf-8") as f:
            for line in f:
                log_content = line.split()
        print(len(log_content),len(current_items))
        if len(log_content) == len(current_items):
            return False
        else: 
            return True



    def setup(self):
        config = folderOrganizer(
            basedir = r'E:\Users\kenne\Downloads',
            folders = self.folders,
            folder_names = self.folder_names
        )
        return config

    def organize(self):
        if self.hasChanged():
            self.setup().setupFolders()
        else:
            print("nope")