import os
import sys

import copy
import logging
import shutil
from logging import getLogger

from babel.messages.pofile import read_po

from babel.messages.pofile import write_po

import convert
from support import parse_args

LOGGER_NAME = "update"

def cli():
    """Command line interface for update script.

    $ ./bin/update cc_org.pot master/cc_org.po

    Updates master/cc_org.po with any new strings found in the PO
    template file.  The PO template can be generated for cc_org
    using i18nextract.
    """

    # get the args
    if len(sys.argv) < 3:
        print "Usage: "
        print "  $ ./bin/update [template file] [master file]"
        print
        sys.exit(-1)

    template_file, master_file = sys.argv[-2:]

    # set up the logging infrastructure
    getLogger(LOGGER_NAME).addHandler(logging.StreamHandler())
    getLogger(LOGGER_NAME).setLevel(logging.INFO)

    # make everything absolute paths
    template_file = os.path.abspath(template_file)
    master_file = os.path.abspath(master_file)

    print template_file
    print master_file

    # load the PO files
    template = read_po(file(template_file, 'r'))
    master = read_po(file(master_file, 'r'))

    # master.update(template, no_fuzzy_matching=True)
    
    for message in template:
        if master.get(message.id, message.context) is None and \
                master.get(message.id) is None:

            # this really isn't in the master file
            master[message.id] = message
            print message.id


    write_po(file(master_file, 'w'), master)
    #        getLogger(LOGGER_NAME).debug("Write %s." % output_fn)
    
