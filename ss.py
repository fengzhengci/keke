import os
from commands import getstatusoutput as getcmd
class aa(object):
    def add_write(self, filename, datalist, pattern='a+'):
        try:
            with open(filename, pattern) as f:
                data = f.read()
                for row in datalist:
                    if row not in data:
                        f.write(row + "\n")
                    continue
        except:
            pass

    def dd(self):
        exclude_list = [
            'linkdood/logs',
            'linkdood/data/bigdata_bak1',
            'linkdood/im/minic/0111miniweb.zip',
            'linkdood/im/minic/20190201_update',
            'linkdood/im/minic/ddio_20190326',
            'linkdood/im/minic/minidood_20190129',
            'linkdood/im/minic/minidood_bak',
            'linkdood/im/minic/miniweb_0111',
            'linkdood/im/minic/miniweb_0116_2',
            'linkdood/im/minic/miniweb_0201',
            'linkdood/im/minic/miniweb0227',
            'linkdood/im/minic/miniweb_1108.tar.gz',
            'linkdood/im/minic/miniweb_1206',
            'linkdood/im/minic/miniweb_20181108.bak',
            'linkdood/im/minic/miniweb_20181128.bak',
            'linkdood/im/minic/miniweb_20190109',
            'linkdood/im/minic/miniweb_20190305.bak',
            'linkdood/im/minic/miniweb_20190326',
            'linkdood/im/minic/miniweb_bak',
            'linkdood/im/minic/miniweb_bak2',
            'linkdood/im/minic/miniweb.tar.gz',
            'linkdood/im/minic/sharecomment_0318.bak'
        ]
        self.add_write("/data/exclude.txt", exclude_list, "w+")
        cmd = "tar -czvf %s -X exclude.txt %s" % ("linkdood.tar.gz", "linkdood")
        getcmd("cd /data/ && " + cmd)

if __name__ == '__main__':
    s = aa()
    s.dd()