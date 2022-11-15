"""
 test_fits2db.py - Unit test for the fitsdb python C extension

 Install the fits2db extension in your current python
 environment, to do so simply run:
    python setup.py install

 To test it simply do:
   pytest test_fits2db.py [-v]
   -v for verbose
"""

__authors__ = 'Igor Sola<igor.suarez-sola@noirlab.edu>'
__version__ = '20221107'  # yyyymmdd

import os
import pytest
import tempfile
from fits2db import fits2db, ArrayException

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# generate a csv file list
# Global variables
temp_file_list = []
fits_files = ["regular_table.fits", "1D_arr.fits", "2D_arr.fits", "3D_arr.fits"]
fits_file_paths = []
fits2db_output_files = ["regular_table.out", "1D_arr.out", "2D_arr.out", "3D_arr.out"]
fits2db_output_file_paths = []
output_files = []


def setup_module():
    global fits_files,fits2db_output_files

    my_path = ROOT_PATH
    for file in fits_files:
        fits_file_paths.append(os.path.join(ROOT_PATH, "data", file))

    for file in fits2db_output_files:
        fits2db_output_file_paths.append(os.path.join(ROOT_PATH, "data", file))


def teardown_module():
    for temp_file in output_files:
        if os.path.isfile(temp_file):
            os.remove(temp_file)


def compare_binaries(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        b1 = f1.read()
        b2 = f2.read()
        return b1 == b2


DDL_TAB_CREATE_1 = 'CREATE TABLE IF NOT EXISTS fits2db_test (\n    "targetid"\tbigint,\n    "targetcode"\ttext,' \
                   '\n    "flux"\tdouble precision\n);\n\n'

DDL_TAB_CREATE_2 = 'CREATE TABLE IF NOT EXISTS fits2db_test (\n    "targetid"	bigint,\n    "targetcode"	text,' \
                   '\n    "fluxarray"	double precision[4]\n);\n\n'

DDL_TAB_CREATE_3 = 'CREATE TABLE IF NOT EXISTS fits2db_test (\n    "targetid"	bigint,\n    "targetcode"	char,' \
                   '\n    "fluxarray"	double precision[4]\n);\n\n'

DDL_TAB_CREATE_4 = 'CREATE TABLE IF NOT EXISTS fits2db_test (\n    "targetid"	bigint,\n    "targetcode"	char,' \
                   '\n    "fluxarray"	double precision[27]\n);\n\n'


@pytest.mark.parametrize(
    "file_pos, tab_create",
    [
        (0, DDL_TAB_CREATE_1, ),
        (1, DDL_TAB_CREATE_2,),
        (2, DDL_TAB_CREATE_3,),
        (3, DDL_TAB_CREATE_4,),
    ])
def test_fits2db(file_pos, tab_create):
    global fits_file_paths, fits2db_output_file_paths, output_files
    temp_fits2db_file = tempfile.NamedTemporaryFile(mode="w", delete=False, dir="/tmp", suffix=".out")
    output_files.append(temp_fits2db_file.name)
    file_in = fits_file_paths[file_pos]
    table_name = "fits2db_test"
    try:
        ddl_command = fits2db(file_in, temp_fits2db_file.name, table_name, True)
        assert ddl_command == tab_create
        assert compare_binaries(fits2db_output_file_paths[file_pos], temp_fits2db_file.name)
    except ArrayException as e:
        # fits2db doesn't support binary output for a fits array. In that case the output
        # will be text.
        try:
          ddl_command = fits2db(file_in, temp_fits2db_file.name, table_name, False)
          assert ddl_command == tab_create
          assert compare_binaries(fits2db_output_file_paths[file_pos], temp_fits2db_file.name)
        except ArrayException as e:
            print("######", str(e))
            assert False
        except Exception as e:
            print("######", str(e))
            assert False
        except SystemError as e:
            print("######", str(e))
            assert False
