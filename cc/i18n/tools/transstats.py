"""
Statistics on the translations of this file.

The CSV written will be in the format of:
  lang,num_messages,num_trans,num_fuzzy,percent_trans
"""

import csv
import optparse
import os
import pkg_resources

from babel.messages.pofile import read_po

CSV_HEADERS = [
    'lang', 'num_messages', 'num_trans', 'num_fuzzy', 'percent_trans']
DEFAULT_INPUT_DIR = pkg_resources.resource_filename(
    'cc.i18n', 'po')
DEFAULT_CSV_FILE = pkg_resources.resource_filename(
    'cc.i18n', 'transstats.csv')


def gen_statistics(input_dir, output_file):
    """
    Generate statistics on languages for how translated they are.

    Keyword arguments:
    - input_dir: The directory of languages we'll iterate through
    - output_file: Path to the CSV file that will be written to
    """
    output_file = file(output_file, 'w')

    input_dir = os.path.abspath(input_dir)
    lang_dirs = os.listdir(input_dir)

    # Create CSV writer
    writer = csv.DictWriter(output_file, CSV_HEADERS)

    # iterate through all the languages
    for lang in sorted(lang_dirs):
        trans_file = os.path.join(input_dir, lang, 'cc_org.po')
        if not os.path.exists(trans_file):
            continue

        # load .po file
        pofile = read_po(file(trans_file, 'r'))

        fuzzies = 0
        translated = 0

        # generate statistics
        for message in pofile:
            if message.string:
                if message.fuzzy:
                    fuzzies += 1
                else:
                    translated += 1

        writer.writerow(
            {'lang': lang,
             'num_messages': len(pofile),
             'num_trans': translated,
             'num_fuzzy': fuzzies,
             'percent_trans': int((float(translated) / len(pofile)) * 100)})

    output_file.close()


def cli():
    """
    Command line interface for transstats
    """
    parser = optparse.OptionParser()

    parser.add_option(
        '-i', '--input_dir', dest='input_dir',
        help='Directory to search for .po files to generate statistics on.',
        default=DEFAULT_INPUT_DIR)
    parser.add_option(
        '-o', '--output_file', dest='output_file',
        help="CSV file we'll write our statistics to.",
        default=DEFAULT_CSV_FILE)

    options, args = parser.parse_args()

    gen_statistics(options.input_dir, options.output_file)


class TransStatsRecipe(object):
    """
    Recipe for running cc.i18n translation statistics.
    """
    def __init__(self, buildout, name, options):
        self.name, self.options = name, options

    def install(self):
        if os.path.exists(DEFAULT_CSV_FILE):
            os.remove(DEFAULT_CSV_FILE)

        gen_statistics(DEFAULT_INPUT_DIR, DEFAULT_CSV_FILE)
        return ()

    update = install


if __name__ == '__main__':
    cli()
