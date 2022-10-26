from distutils.core import setup, Extension

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
          author="Igor Suarez",
          author_email="igor.suarez-sola@noirlab.edu",
          ext_modules=[fits2db_ext])

if __name__ == "__main__":
    main()
