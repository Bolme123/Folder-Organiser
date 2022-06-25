import execute
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os
downloads_path = str(Path.home() / "Downloads")

class isDownload:
    def __init__(self):
        self.download_time = time.time()

class Watcher:
    DIRECTORY_TO_WATCH = downloads_path

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print( "Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    partDownloadTime = 0
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            extension = os.path.splitext(event.src_path)[-1]
            if extension == ".part":
                initialSize = 0
                currentSize = 0
                counter = 0
                while True:
                    fileExists = os.path.exists(event.src_path)
                    if not fileExists:
                        if counter > 1: 
                            Handler.partDownloadTime = time.time()
                        break
                    else:
                        try: 
                            if initialSize == 0:
                                Handler.partDownloadTime = time.time()
                                initialSize = os.path.getsize(event.src_path)
                                time.sleep(0.1)
                            
                            currentSize = os.path.getsize(event.src_path)
                            print(currentSize,initialSize)
                            time.sleep(3)
                        except FileNotFoundError:
                            print("%s  not found, continuing..." % event.src_path)
                            break
            else:
                if time.time() - Handler.partDownloadTime <= 6:
                    o = execute.DownloadOrganize()
                    o.organize()


if __name__ == '__main__':
    w = Watcher()
    w.run()