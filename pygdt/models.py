from collections import OrderedDict
import time

class GDTRecord(object):

    def __init__(self):
        self.fields = None

        self.field_map = {
            8000: ('sentence_id', int),
            8010: ('sentence_length', int),
            9218: ('gdt_version', float),
            
            3000: ('patient_id', str),
            3101: ('patient_last_name', str),
            3102: ('patient_first_name', str),
            3103: ('patient_birth_date', str),
            3110: ('patient_sex', str),

            6200: ('data_date', str),
            6201: ('data_time', str),
            8402: ('device', str),
            8432: ('reading_date', str),
            8439: ('reading_time', str),
        }

    def read_file(self, path):
        fields = []
        
        try:
            raw_data = open(path, 'rb').read()
        except PermissionError:
            # TODO: make this Windows fix more robust - 5 retries
            time.sleep(1)
            raw_data = open(path, 'rb').read()

        
        #TODO: make configurable 'utf-8', 'latin-1', 'cp437'
        try:
            data = raw_data.decode('latin-1')
        except UnicodeDecodeError:
            raise

        for line in data.splitlines():
            fields += (self.parse_line(line),)
        self.fields = OrderedDict(fields)
        self.parse_data()

    def parse_line(self, line):
        length = int(line[0:3])
        field_id = int(line[3:7])
        data = line[7:length]

        return (field_id, {
            'length': length,
            'data': data.strip(),
        })

    def parse_data(self):
        for field_id in self.field_map.keys():
            try:
                setattr(
                    self,
                    self.field_map[field_id][0],
                    self.field_map[field_id][1](self.fields[field_id]['data'])
                )
            except:
                setattr(
                    self,
                    self.field_map[field_id][0],
                    None
                )

    def dump(self):
        from pprint import pprint

        for value in self.field_map.values():
            print("{}: {}".format(value[0], getattr(self, value[0], "")))
        print("Raw data:")
        for f in self.fields.items():
            pprint(f)
        print("")
