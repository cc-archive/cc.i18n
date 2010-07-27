import os
import logging
from logging import getLogger
import pkg_resources

from babel.messages.pofile import read_po
from babel import localedata
from babel import core

from babel.messages.pofile import write_po

from cc.i18n.tools import convert
from cc.i18n.tools.support import parse_args
import sha

LOGGER_NAME = "po2cc"


INPUT_DIR = pkg_resources.resource_filename(
    'cc.i18n', 'po')
OUTPUT_DIR = pkg_resources.resource_filename(
    'cc.i18n', 'i18n')
MASTER_PO = pkg_resources.resource_filename(
    'cc.i18n', 'master/cc_org.po')

def po2cc(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR,
          english_po=MASTER_PO, verbosity=logging.WARNING,
          cache=True):
    # set up the logging infrastructure
    getLogger(LOGGER_NAME).addHandler(logging.StreamHandler())
    getLogger(LOGGER_NAME).setLevel(verbosity)

    # make everything absolute paths
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    english_po = os.path.abspath(english_po)

    for root, dirnames, filenames in os.walk(input_dir):
        
        for fn in filenames:

            # only process .po files
            if fn[-3:] != '.po': continue
            input_fn = os.path.join(root, fn)

            getLogger(LOGGER_NAME).info("Processing %s." % input_fn)

            # determine the output path
            output_fn = os.path.join(
                output_dir,
                input_fn[len(input_dir) + 1:])

            # make sure the necessary directories exist
            if not(os.path.exists(os.path.dirname(output_fn))):
                os.makedirs(os.path.dirname(output_fn))

            # grab the locale from the path
            locale_code = root.split(os.sep)[-1]
            if localedata.exists(locale_code):
                locale = core.Locale.parse(locale_code)
            # fallback to parent language
            elif '-' in locale_code and localedata.exists(locale_code.split('_')[0]):
                locale = core.Locale.parse(locale_code.split('_')[0])                
            else:
                locale = None

            # optional: if caching enabled, and we have processed our files before, don't do anything
            if cache:
                cache_dir = os.path.join(os.getenv('HOME'), '.cc2po-cache')
                if not os.path.exists(cache_dir):
                    os.mkdir(cache_dir, 0700)
                input_sha1 = sha.sha(open(input_fn).read()).hexdigest()
                input_sha_file = os.path.join(cache_dir, input_sha1)
                if os.path.exists(input_sha_file):
                    # if it exists, check the file's contents.
                    output_sha1 = sha.sha(open(output_fn).read()).hexdigest()
                    contents = open(input_sha_file).read().strip()
                    if contents == output_sha1:
                        getLogger(LOGGER_NAME).info('Due to caching, we have skipped this file.')
                        continue # we have previously recorded that this is the right output

            # convert the file
            result = convert.po_to_cc(read_po(file(input_fn, 'r'),
                                              locale, 
                                              'cc_org'),
                             read_po(file(english_po, 'r')))

            convert.defuzz(result)

            write_po(file(output_fn, 'w'), result)
            getLogger(LOGGER_NAME).debug("Write %s." % output_fn)

            # if caching is enabled, store a note that the result is good
            if cache:
                assert input_sha1 == sha.sha(open(input_fn).read()).hexdigest()
                input_sha_file = os.path.join(cache_dir, input_sha1)
                output_sha1 = sha.sha(open(output_fn).read()).hexdigest()
                fd = open(input_sha_file, 'w')
                fd.write(output_sha1)
                fd.close()


def cli():
    """Command line interface for po2cc script."""

    # parse the command line
    (options, args) = parse_args(
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR)

    po2cc(options.input_dir, options.output_dir,
          options.english_po, options.verbosity, options.cache)


class Po2CC(object):
    def __init__(self, buildout, name, options):
        self.name, self.options = name, options

    def install(self):
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)

        po2cc()
        return OUTPUT_DIR

    def update(self):
        po2cc()
