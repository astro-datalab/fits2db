
# FITS2DB -- Convert FITS Binary Tables to Database formats


##  Usage:

    fits2db [<opts>] [ <input> ... ]

where <opts> include:

```
      -h,--help                this message
      -d,--debug               set debug flag
      -v,--verbose             set verbose output flag
      -n,--noop                set no-op flag

                                   INPUT PROCESSING OPTIONS
      -c,--chunk=<N>           process <N> rows at a time
      -e,--extnum=<N>          process table in FITS extension number <N>
      -E,--extname=<name>      process table in FITS extension name <name>
      -i,--input=<file>        set input filename
      -o,--output=<file>       set output filename
      -r,--rowrange=<range>    convert rows within given <range>
      -s,--select=<expr>       select rows based on <expr>

                                   PROCESSING OPTIONS
      -C,--concat              concatenate all input files to output
      -H,--noheader            suppress CSV column header
      -N,--nostrip             don't strip strings of whitespace
      -Q,--noquote             don't quote strings in text formats
      -S,--singlequote         use single quotes for strings
      -X,--explode             explode array cols to separate columns

                                   FORMAT OPTIONS
      --asv                    output an ascii-separated value table
      --bsv                    output a bar-separated value table
      --csv                    output a comma-separated value table
      --tsv                    output a tab-separated value table
      --ipac                   output an IPAC formatted table

                                   SQL OPTIONS
      -B,--binary              output binary SQL
      -t,--table=<name>        create table named <name>
      -Z,--noload              don't create table load commands

      --sql=<db>               output SQL correct for <db> type
      --drop                   drop existing DB table before conversion
      --create                 create DB table from input table structure
      --truncate               truncate DB table before loading
```


##  Examples:

    1)  Load all FITS tables in directory to a new Postgres database table
        named 'mytab' in binary mode, expanding arrays to new columns::

        % fits2db --sql=postgres --create -B -C -X -t mytab *.fits | psql

    2)  Replace the contents of the database table 'mytab' with the contents
        of the named FITS files:

        % fits2db --sql=postgres --truncate -t mytab new.fits | psql
            or
        % fits2db --sql=postgres --drop --create -t mytab new.fits | psql

    3)  Convert all FITS tabes to ascii SQL files using the file root name:

        % fits2db --sql=mysql --create *.fits           # for MySQL
        % fits2db --sql=sqlite --create *.fits          # for SQLite
        % fits2db --sql=postgres --create *.fits        # for PostgresQL

    4)  Convert FITS bintable to CSV on the standard output:

        % fits2db --csv test.fits

        Suppress the CSV column header:

        % fits2db --csv --noheader test.fits

        Use single quotes on strings and don't strip leading/trailing spaces,
        create an output file 'test.csv':

        % fits2db --csv --singlequote --nostrip -o test.csv test.fits

    5)  Create a database table based on the structure of the FITS bintable
        but don't actually load the data:

        % fits2db --sql=postgres --create --noload -t mytab test.fits


Additionally, filename modifiers may be added in order to select the
specific file extension or filter the table for specific rows or columns.
Examples of this type of filtering include:

    fits2db tab.fits[sci]                  - list the 'sci' extension
    fits2db tab.fits[1][#row < 101]        - list first 100 rows of extn 1
    fits2db tab.fits[col X;Y]              - list X and Y cols only
    fits2db tab.fits[col -PI,-ETA]         - list all but the PI and ETA cols
    fits2db tab.fits[col -PI][#row < 101]  - combined case

For details on table row and column filtering, see CFITSIO documentation.


