'''
sqldumpr -- functions to generate a SQL dump from a SQL statement on CartoDB
'''

import requests

TYPE_MAP = {
    'string': 'TEXT',
    'number': 'NUMERIC',
    'geometry': 'GEOMETRY',
    'JSON': 'JSON',
}

class Dumpr(object):

    def __init__(self, hostname, api_key):
        self._hostname = hostname
        self._api_key = api_key

    @property
    def _url(self):
        return 'https://{hostname}/api/v2/sql'.format(
            hostname=self._hostname
        )

    def query(self, q, **options):
        '''
        Query the account.  Returned is the response, wrapped by the requests
        library.
        '''
        params = options.copy()
        params['q'] = q
        return requests.get(self._url, params=params)

    def dump(self, query, tablename, writable):
        '''
        '''
        query_limit_zero = query + ' LIMIT 0'
        resp = self.query(query_limit_zero)
        coltypes = dict([
            (k, TYPE_MAP[v['type']]) for k, v in resp.json()['fields'].iteritems()
        ])
        resp = self.query(query_limit_zero, format='csv')
        colnames = resp.text.strip().split(',')
        columns = ', '.join(['{colname} {type}'.format(
            colname=c,
            type=coltypes[c]
        ) for c in colnames])
        create_table = '''DROP TABLE IF EXISTS {tablename};

        CREATE TABLE {tablename} (
            {columns}
        );\n\n'''.format(
            tablename=tablename, columns=columns)
        resp = self.query(query, format='csv')

        writable.write(create_table)
        writable.write('COPY {tablename} FROM stdin WITH CSV HEADER;\n'.format(
            tablename=tablename
        ))
        for line in resp.iter_lines():
            if not line:
                continue
            writable.write(line + '\n')
        writable.write('\\.\n')
