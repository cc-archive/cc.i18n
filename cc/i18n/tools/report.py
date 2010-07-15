import os
import copy
import shutil
from logging import getLogger
import pkg_resources

from babel.messages.pofile import read_po

from babel.messages.pofile import write_po

from cc.i18n.tools import convert
from cc.i18n.tools.support import parse_args

def count(catalog):
    """Given a Catalog, return the number of strings actually translated."""

    translated = [m for m in 
                  catalog
                  if m.string]

    return len(translated)

def cli():
    """Command line interface for report script."""

    # parse the command line
    (options, args) = parse_args(
        input_dir=pkg_resources.resource_filename(
            'cc.i18n', 'po'),
        output_dir=pkg_resources.resource_filename(
            'cc.i18n', 'po'))

    # make everything absolute paths
    options.input_dir = os.path.abspath(options.input_dir)

    # load the master domain file and count the available messages
    master = float(count(read_po(file(options.english_po, 'r'))))

    progress = {}

    # walk the input directory...
    for root, dirnames, filenames in os.walk(options.input_dir):
        
        # ...looking for .po files
        for fn in filenames:

            # only process .po files
            if fn[-3:] != '.po': continue
            input_fn = os.path.join(root, fn)

            progress[root.split('/')[-1]] = \
                count(read_po(file(input_fn, 'r'))) / master * 100

    # sort the results by percent complete
    progress = [(progress[n], n) for n in progress]
    progress.sort()
    progress.reverse()

    for locale in progress:
        print "%*.1f %%    %s" % (8, locale[0], locale[1])

