# import time module, Observer, FileSystemEventHandler
import time,os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path




class OnMyWatch:
    # Set the directory on watch
    
    watchDirectory = str(Path.home() / "Downloads/")

  
    def __init__(self):
        self.observer = Observer()
  
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
  
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
  
    @staticmethod
    def on_any_event(event):


        if event.event_type == 'modified':
            # Event is modified, you can process it now
            if str(event.src_path[-4:]) == "part":
                pass
            else:
                filesize = -1
                while filesize != os.path.getsize(event.src_path):
                    print("Downloading")
                    filesize = os.path.getsize(event.src_path)
                    time.sleep(1)
                print("DONE!")

              
  
if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()