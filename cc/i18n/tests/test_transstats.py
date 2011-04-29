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

    csv_file_lines = set(file(csv_file_path).read().strip().splitlines())
    assert csv_file_lines == set(
        ['en,564,0,1,0', 'es,564,550,7,97', 
         'pt,564,552,6,97', 'pt_BR,564,381,13,67', 'pt_PT,564,338,25,59',
         'vi,564,459,18,81', ])
