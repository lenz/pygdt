from file import observe_gdt_folder

if __name__ == "__main__":

    def callback(record=None, event=None):
        print("File: %s" % event.src_path)
        print("Event: %s" % event.event_type)
        record.dump()
        print("")

    path = './'
    patterns = ["*.gdt"]
    print("observing %s for patterns: %s\n" % (path, patterns))
    observe_gdt_folder(path=path, patterns=patterns, callback=callback)
