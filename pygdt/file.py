from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from pygdt.models import GDTRecord

import time


class GDTFileHandler(PatternMatchingEventHandler):

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback')

        super(GDTFileHandler, self).__init__(args, kwargs)

    def dispatch(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        if not event.is_directory:
            record = GDTRecord()
            record.read_file(event.src_path)
            self.callback(record, event)


def observe_gdt_folder(path=None, patterns=None, callback=None):
    observer = Observer()
    observer.schedule(
        GDTFileHandler(
            patterns=patterns,
            callback=callback
        ),
        path=path,
        recursive=False
    )
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
