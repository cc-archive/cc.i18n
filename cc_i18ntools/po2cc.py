import os
import logging
from logging import getLogger

from babel.messages.pofile import read_po, write_po

import convert
from support import parse_args

LOGGER_NAME = "po2cc"

def cli():
    """Command line interface for po2cc script."""

    # parse the command line
    (options, input_files) = parse_args(input_dir = 'po',
                                        output_dir = 'i18n')

    # set up the logging infrastructure
    getLogger(LOGGER_NAME).addHandler(logging.StreamHandler())
    getLogger(LOGGER_NAME).setLevel(options.verbosity)

    # make everything absolute paths
    options.input_dir = os.path.abspath(options.input_dir)
    options.output_dir = os.path.abspath(options.output_dir)
    options.english_po = os.path.abspath(options.english_po)

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

            # convert the file
            result = convert.po_to_cc(read_po(file(input_fn, 'r')),
                             read_po(file(options.english_po, 'r')))

            write_po(file(output_fn, 'w'), result)
            getLogger(LOGGER_NAME).debug("Write %s." % output_fn)

