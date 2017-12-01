from builtins import open
import os
import pkg_resources
import tempfile

from cc.i18n.tools import transstats


def test_gen_statistics():
    """
    Test the translation statistics generating gen_statistics func.
    """
    temp_dir = tempfile.mkdtemp()
    csv_file_path = os.path.join(temp_dir, 'transstats.csv')

    fake_podir = pkg_resources.resource_filename('cc.i18n.tests', 'fake_podir')

    transstats.gen_statistics(fake_podir, csv_file_path)

    csv_file_lines = set(open(csv_file_path).read().strip().splitlines())
    assert csv_file_lines == set(
        ['pt_BR,559,376,13,67', 'es,559,545,7,97', 'pt,559,547,6,97',
         'vi,559,454,18,81', 'en,559,0,1,0'])
