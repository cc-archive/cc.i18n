import os
import copy
import logging
import shutil
from logging import getLogger
import pkg_resources

from babel.messages.pofile import read_po, write_po

from cc.i18n.tools import convert
from cc.i18n.tools.support import parse_args

LOGGER_NAME = "sync"
PO_DIR = pkg_resources.resource_filename('cc.i18n', 'po')


def sync(input_dir, output_dir, english_po, verbosity=logging.WARNING):
    """
    Sync new messages / changed messages across all po files

    Keyword arguments:
    - input_dir: The directory with files that have the old translations
    - output_dir: The directory where we will write files with updated
      translations
    - english_po: The english .po file, which we'll look at for reference
    - verbosity: How noisy we should be in our logging (default logging.WARNING)
    """
    # set up the logging infrastructure
    getLogger(LOGGER_NAME).addHandler(logging.StreamHandler())
    getLogger(LOGGER_NAME).setLevel(verbosity)

    # make everything absolute paths
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    english_po = os.path.abspath(english_po)

    # load the master domain file
    master = read_po(file(english_po, 'r'))
    previous_master = read_po(file(english_po + '.bak', 'r'))

    # walk the input directory...
    for root, dirnames, filenames in os.walk(input_dir):
        
        # ...looking for .po files
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

            # load the source file
            source = read_po(file(input_fn, 'r'))

            # convert the source back to cc-style 
            # (so we can match symbolic names)
            source = convert.po_to_cc(source, previous_master,
                                      fallback=False)

            # add any new string from the master
            for message in master:
                
                # don't add strings that don't have an ID
                if not message.id:
                    continue

                if message.id not in source:
                    # copy the Message object
                    source[message.id] = copy.deepcopy(message)

                    # new strings aren't translated by default
                    source.get(message.id, message.context).string = ""

                # If for some reason python-format ended up in
                # source's message but wasn't in master's message
                # (probably due to auto-detection by babel), remove it
                # from source's message.
                if (('python-format' in source[message.id].flags and
                     'python-format' not in message.flags)):
                    source[message.id].flags.remove('python-format')

            # convert back to .po style, thereby updating the English source
            source = convert.cc_to_po(source, master, previous_master)

            write_po(file(output_fn, 'w'), source, width=None)
            getLogger(LOGGER_NAME).debug("Write %s." % output_fn)

    # copy master to previous_master
    shutil.copyfile(english_po, '%s.bak' % english_po)
    

def cli():
    """Command line interface for sync script."""

    # parse the command line
    (options, args) = parse_args(
        input_dir=PO_DIR,
        output_dir=PO_DIR)

    sync(options.input_dir, options.output_dir, options.english_po,
         options.verbosity)


if __name__ == '__main__':
    cli()
