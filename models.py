from collections import OrderedDict


class GDTRecord(object):

    def __init__(self):
        self.fields = None

        self.field_map = {
            8000: ('type', int),
            9218: ('version', float),
            3101: ('last_name', str),
            3102: ('first_name', str)
        }

    def read_file(self, path):
        fields = []
        for line in open(path, 'r'):
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
            print("%s: %s" % (value[0], getattr(self, value[0], "")))
        print("Raw data:")
        for f in self.fields.items():
            pprint(f)
