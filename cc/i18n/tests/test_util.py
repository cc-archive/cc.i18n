import os
import tempfile

from cc.i18n import util


def test_get_all_trans_stats():
    """
    Test the get_all_trans_stats utility function.
    """
    temp_dir = tempfile.mkdtemp()

    # write a fake CSV file
    transstats = os.path.join(temp_dir, 'transstats.csv')
    ts_file = file(transstats, 'w')
    ts_file.write(
        ('es_AR,564,343,27,60\n'
         'en_US,564,0,1,0\n'
         'hr,564,447,17,79\n'
         'no,564,400,14,70'))
    ts_file.close()

    expected = {
        'es_AR': {
            'num_messages': 564,
            'num_trans': 343,
            'num_fuzzy': 27,
            'num_untrans': 194,
            'percent_trans': 60},
        'en_US': {
            'num_messages': 564,
            'num_trans': 0,
            'num_fuzzy': 1,
            'num_untrans': 563,
            'percent_trans': 0},
        'hr': {
            'num_messages': 564,
            'num_trans': 447,
            'num_fuzzy': 17,
            'num_untrans': 100,
            'percent_trans': 79},
        'no': {
            'num_messages': 564,
            'num_trans': 400,
            'num_fuzzy': 14,
            'num_untrans': 150,
            'percent_trans': 70}}

    results = util.get_all_trans_stats(transstats)
    assert results == expected

    # overwrite that old CSV file,
    ts_file = file(transstats, 'w')
    ts_file.write(
        ('es_AR,999,999,999,999\n'
         'en_US,999,999,999,999\n'
         'hr,999,999,999,999\n'
         'no,999,999,999,999'))
    ts_file.close()

    # make sure it cached the old results
    results = util.get_all_trans_stats(transstats)
    assert results == expected
