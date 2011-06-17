import os
import logging
from logging import getLogger
import pkg_resources

from babel.messages.pofile import read_po

from cc.i18n.tools import convert
from cc.i18n.tools.support import parse_args, polib_wrapped_write_po

LOGGER_NAME = "cc2po"

INPUT_DIR = pkg_resources.resource_filename(
    'cc.i18n', 'i18n')
OUTPUT_DIR = pkg_resources.resource_filename(
    'cc.i18n', 'po')
MASTER_PO = pkg_resources.resource_filename(
    'cc.i18n', 'master/cc_org.po')


def cc2po(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR,
          english_po=MASTER_PO, verbosity=logging.WARNING):
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

            # convert the file
            result = convert.cc_to_po(read_po(file(input_fn, 'r')),
                             read_po(file(english_po, 'r')))

            polib_wrapped_write_po(output_fn, result)
            getLogger(LOGGER_NAME).debug("Write %s." % output_fn)


def cli():
    """Command line interface for cc2po script."""

    # parse the command line
    (options, input_files) = parse_args()

    cc2po(options.input_dir, options.output_dir,
          options.english_po, options.verbosity)
