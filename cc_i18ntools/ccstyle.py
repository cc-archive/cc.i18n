import os
import optparse
import copy
import logging
from logging import getLogger

from babel.messages.pofile import read_po, write_po
from babel.messages.catalog import Catalog, Message

LOGGER_NAME = "ccstyle"

def reverse_english(message, english):
    """Look for the key of [message] (an instance of Message) as the string
    of a message in [english] (an instance of Catalog).  If found, return
    a new message whose key is the same as the English key.  If not found,
    return the original message."""

    for en_msg in english:
        if en_msg.string == message.id:
            # found it!
            result = copy.deepcopy(message)
            result.id = en_msg.id
            return result

    return copy.deepcopy(message)

def po_to_cc(source, english):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Message strings in [english]; if a 
    match is found, the key is replaced with the key from the [english] match.
    The result is a Catalog whose keys are symbolic rather than English text.

    Returns a Catalog instance."""

    # create the new target Catalog
    target = Catalog()

    # iterate over all the strings in the target PO
    for message in source:
        new_message = reverse_english(message, english)

        target[new_message.id] = new_message

    return target

def cc_to_po(source, english):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Messages in [english].  If a Message
    with the same ID is found in [english], the ID is replaced with the 
    English text.  The result is a Catalog whose keys contain English text
    rather than symbolic strings.

    Returns a Catalog instance."""

def make_option_parser():
    """Return an optparse.OptionParser configured for the make_cc_files 
    command line script."""

    parser = optparse.OptionParser()

    # settings
    parser.add_option('-e', '--english', dest='english_po',
                      default='i18n/en/cc_org.po',
                      help='English .po file, used to map keys.')

    # input options
    parser.add_option('-i', '--input-dir', dest='input_dir',
                      default='i18n',
                      help='Directory to search for .po files to convert.')

    # output options
    parser.add_option('-o', '--output-dir', dest='output_dir', 
                      default='cc_i18n',
                      help='Output directory for CC-style .po files.')

    return parser

def cli():
    """Command line interface for make_cc_files script."""

    # set up the logging infrastructure
    getLogger(LOGGER_NAME).addHandler(logging.StreamHandler())
    getLogger(LOGGER_NAME).setLevel(logging.INFO)

    # parse the command line
    (options, input_files) = make_option_parser().parse_args()

    options.input_dir = os.path.abspath(options.input_dir)
    options.output_dir = os.path.abspath(options.output_dir)
    options.english_po = os.path.abspath(options.english_po)

    for root, dirnames, filenames in os.walk(options.input_dir):
        
        for fn in filenames:

            # only process non-English .po files
            if fn[-3:] != '.po': continue
            input_fn = os.path.join(root, fn)
            if input_fn == options.english_po:
                continue

            # determine the output path
            output_fn = os.path.join(
                options.output_dir,
                input_fn[len(options.input_dir) + 1:])

            # make sure the necessary directories exist
            if not(os.path.exists(os.path.dirname(output_fn))):
                os.makedirs(os.path.dirname(output_fn))

            # convert the file
            convert_file(input_fn, output_fn, options.english_po)

