from distutils.core import setup, Extension

# This setup file assumes that the fitsio include file fitsio.h lives in
# /usr/local/include
# By the same token the library libcfitsio.a lives # in /usr/local/lib
# If your installation differs from this, then change /usr/local/include
# and lib paths below to reflect your fitsio installation.

def main():

    fits2db_ext = Extension('fits2db',
                        define_macros = [('PYTHON_EXT', '1')],
                        include_dirs = ['/usr/local/include', './'],
                        libraries = ['cfitsio'],
                        library_dirs = ['/usr/local/lib'],
                        sources = ['fits2db.c'])

    setup(name="fits2db",
          version="1.0.0",
          description="Python interface to prepare fits file for DB import ",
          author="Igor Suarez (Extension), Mike Fitzpatrick (FITS2DB)",
          author_email="igor.suarez-sola@noirlab.edu, mike.fitzpatrick@noirlab.edu",
          ext_modules=[fits2db_ext])

if __name__ == "__main__":
    main()
