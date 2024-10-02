import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scanner import scan_files, index_files
import os

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            root_directory = '/home/aaron/projects/test-data/Semester'  # Ersetzen Sie diesen Pfad entsprechend
            scan_files(root_directory)
            index_files()

    def on_created(self, event):
        if not event.is_directory:
            root_directory = '/home/aaron/projects/test-data/Semester'  # Ersetzen Sie diesen Pfad entsprechend
            scan_files(root_directory)
            index_files()

if __name__ == "__main__":
    root_directory = '/home/aaron/projects/test-data/Semester'  # Ersetzen Sie diesen Pfad entsprechend
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=root_directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()