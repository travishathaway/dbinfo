import json
import csv
import sys


class Dbinfo(object):

    '''
    Base class to use for dbms specific classes
    '''

    def __init__(self, config, outfile=None):
        pass

    def _format_csv(self, headers=None):
        rows = self.cur.fetchall()

        if self.outfile:
            with open('%s.csv' % self.outfile, 'w') as csv_file:
                self._write_csv(csv_file, rows, headers=headers)
        else:
            self._write_csv(sys.stdout, rows, headers=headers)

    def _write_csv(self, target, rows, headers=None):
        csv_file = csv.writer(target, delimiter=',',
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if headers:
            csv_file.writerow(headers)

        for row in rows:
            csv_file.writerow([col for col in row])

    def _format_json(self):
        results = self.cur.fetchall()

        if self.outfile:
            with open('%s.json' % self.outfile, 'w') as json_file:
                json_file.write(self._write_json(results))
        else:
            sys.stdout.write(self._write_json(results))

    def _write_json(self, results):
        return json.dumps(results)
