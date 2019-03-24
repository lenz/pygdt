from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pygdt.models import GDTRecord
from slugify import slugify

import time
import os


class GDTFileHandler(FileSystemEventHandler):

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback')
        self.file = kwargs.pop('file')
        self.folder = kwargs.pop('folder')
        self.last_modified = {}

        super(GDTFileHandler, self).__init__(*args, **kwargs)

    def dispatch(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        if event.is_directory:
            return
        if event.event_type not in ['modified', 'created']:
            return
        if os.path.split(event.src_path)[1] != self.file:
            return

        def do_callback():
            self.last_modified[pathid] = modified
            record = GDTRecord()
            record.read_file(event.src_path)
            self.callback(record, event)

        fullpath = os.path.join(self.folder, self.file)
        pathid = slugify(fullpath)
        modified = os.stat(fullpath).st_mtime

        # prevent double event
        if pathid in self.last_modified:
            if (modified - self.last_modified[pathid] > 0.1):
                do_callback()
            else:
                print("--> {modified} - preventing double event - time diff: {diff}\n".format(
                    modified=modified,
                    diff=modified - self.last_modified[pathid]
                ))
        else:
            do_callback()


def observe_gdt_files(files=None, callback=None):
    observer = Observer()
    for file_path in files:
        folder, file = os.path.split(file_path)
        observer.schedule(
            GDTFileHandler(
                file=file,
                folder=folder,
                callback=callback
            ),
            path=folder
        )
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
