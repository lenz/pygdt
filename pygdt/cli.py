from pygdt.file import observe_gdt_folder

def main():
    

    def callback(record=None, event=None):
        print("File: {}".format(event.src_path))
        print("Event: {}".format(event.event_type))
        record.dump()
        print("")

    path = './'
    patterns = ["*.gdt"]
    print("observing {} for patterns: {}\n".format(path, patterns))
    observe_gdt_folder(path=path, patterns=patterns, callback=callback)