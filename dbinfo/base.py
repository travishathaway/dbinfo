import json
import csv


class Dbinfo(object):

    '''
    Base class to use for dbms specific classes
    '''

    def __init(self, config):
        pass

    def _format_csv(self, report_name='default'):
        results = self.cur.fetchall()

        with open('%s.csv' % report_name, 'w') as csv_file:
            csv_file = csv.writer(csv_file, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_file.writerow(['Database Name', 'Size (MB)'])

            for row in results:
                csv_file.writerow([row[0], row[1]])

    def _format_json(self, report_name='default'):
        results = self.cur.fetchall()

        with open('%s.json' % report_name, 'w') as json_file:
            json_file.write(json.dumps(results))
