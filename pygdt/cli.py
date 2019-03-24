from pygdt.file import observe_gdt_files
import sys


def main():

    def callback(record=None, event=None):
        print("File: {}".format(event.src_path))
        print("Event: {}".format(event.event_type))
        record.dump()
        print("")

    print("observing files: {}\n".format(sys.argv[1:]))

    observe_gdt_files(
        files=sys.argv[1:],
        callback=callback
    )
