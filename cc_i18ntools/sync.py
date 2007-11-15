import os
import logging
from logging import getLogger

from babel.messages.pofile import read_po, write_po

import convert
import support

LOGGER_NAME = "sync"

def make_option_parser():
    """Return an optparse.OptionParser configured for the sync
    command line script."""

    parser = support.make_option_parser()
    parser.set_defaults(input_dir = 'i18n',
                        output_dir = 'i18n')

    return parser


def cli():
    """Command line interface for sync script."""

    # parse the command line
    (options, args) = make_option_parser().parse_args()

    # set up the logging infrastructure
    getLogger(LOGGER_NAME).addHandler(logging.StreamHandler())
    getLogger(LOGGER_NAME).setLevel(options.verbosity)

    # make everything absolute paths
    options.input_dir = os.path.abspath(options.input_dir)
    options.output_dir = os.path.abspath(options.output_dir)
    options.english_po = os.path.abspath(options.english_po)

    # translate the master file using itself 
    # (ie, so the strings and keys are the same)
    master = read_po(file(options.english_po, 'r'))
    master = convert.cc_to_po(master, master)

    for root, dirnames, filenames in os.walk(options.input_dir):
        
        for fn in filenames:

            # only process .po files
            if fn[-3:] != '.po': continue
            input_fn = os.path.join(root, fn)

            getLogger(LOGGER_NAME).info("Processing %s." % input_fn)

            # determine the output path
            output_fn = os.path.join(
                options.output_dir,
                input_fn[len(options.input_dir) + 1:])

            # make sure the necessary directories exist
            if not(os.path.exists(os.path.dirname(output_fn))):
                os.makedirs(os.path.dirname(output_fn))

            # merge it with the translated master 
            # (babel handles the fuzzy matching)

            # convert the file
            source = read_po(file(input_fn, 'r'))
            source.update(master)

            write_po(file(output_fn, 'w'), source)
            getLogger(LOGGER_NAME).debug("Write %s." % output_fn)



