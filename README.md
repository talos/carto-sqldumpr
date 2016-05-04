# carto-sqldumpr

Simple script to generate an SQL dump from a SQL statement executed on
a CartoDB account.

### Example usage

To create an SQL dump of `obs_table` from the Observatory into a file called
`dump.sql` in the current working directory:

    from sqldumpr import Dumpr

    hostname='observatory.cartodb.com'
    api_key=''

    d = Dumpr(hostname, api_key)
    d.dump('SELECT * FROM obs_table', 'obs_table', 'dump.sql')
