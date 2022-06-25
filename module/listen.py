import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os, sys

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "Download_Organizer"
    _svc_display_name_ = "Download Organizer"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        sys.path.append(os.path.abspath(r'C:\Users\kenne\OneDrive\Kode\Python\Folder Organiser'))
        import execute
        def on_created(event):
            time.sleep(2)
            k = execute.setup()
            k.setupFolders()
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = True
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = on_created

        path = os.path.abspath("E:/Users/kenne/Downloads")
        go_recursively = False
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=False)

        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()



if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)



