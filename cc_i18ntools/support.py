import logging
import optparse

def make_option_parser():
    """Return an optparse.OptionParser configured for the make_cc_files 
    command line script."""

    parser = optparse.OptionParser()
    parser.set_defaults(verbosity=logging.WARNING)

    # settings
    parser.add_option('-m', '--master', dest='english_po',
                      default='master/cc_org.po',
                      help='Master .po file, used to map keys.')
    parser.add_option('-q', '--quiet', dest='verbosity',
                      action='store_const', const=logging.ERROR)
    parser.add_option('-v', dest='verbosity', 
                      action='store_const', const=logging.INFO)
    parser.add_option('--noisy', dest='verbosity', 
                      action='store_const', const=logging.DEBUG)

    # input options
    parser.add_option('-i', '--input-dir', dest='input_dir',
                      help='Directory to search for .po files to convert.')

    # output options
    parser.add_option('-o', '--output-dir', dest='output_dir', 
                      help='Output directory for CC-style .po files.')

    return parser

def parse_args(**defaults):
    """Parse the optoins and arguments from the command-line and make sure
    required values are present.  [defaults] is a dict containing the default
    values to pass to the parser.

    Returns a two tuple: (options, args).
    """

    parser = make_option_parser()
    parser.set_defaults(**defaults)


    options, args = parser.parse_args()

    # make sure an input and output directory were specified
    if not(options.input_dir):
        parser.error("An input directory must be supplied.")
    
    if not(options.output_dir):
        parser.error("An output directory must be supplied.")


    return options, args

"""
***************************************************************************
***************************************************************************

Slightly modified version of write_po, based on the Babel 0.9.1 version.
This version does not attempt to join locations, thereby avoiding a problem
with word-wrapping.

See http://babel.edgewall.org/ticket/73

***************************************************************************
***************************************************************************
"""

from datetime import date, datetime
import os
import re
try:
    set
except NameError:
    from sets import Set as set
from textwrap import wrap

from babel import __version__ as VERSION
from babel.messages.catalog import Catalog, Message
from babel.messages.pofile import normalize
from babel.util import LOCALTZ

def write_po(fileobj, catalog, width=76, no_location=False, omit_header=False,
             sort_output=False, sort_by_file=False, ignore_obsolete=False,
             include_previous=False):
    r"""Write a ``gettext`` PO (portable object) template file for a given
    message catalog to the provided file-like object.

    >>> catalog = Catalog()
    >>> catalog.add(u'foo %(name)s', locations=[('main.py', 1)],
    ...             flags=('fuzzy',))
    >>> catalog.add((u'bar', u'baz'), locations=[('main.py', 3)])
    >>> from StringIO import StringIO
    >>> buf = StringIO()
    >>> write_po(buf, catalog, omit_header=True)
    >>> print buf.getvalue()
    #: main.py:1
    #, fuzzy, python-format
    msgid "foo %(name)s"
    msgstr ""
    <BLANKLINE>
    #: main.py:3
    msgid "bar"
    msgid_plural "baz"
    msgstr[0] ""
    msgstr[1] ""
    <BLANKLINE>
    <BLANKLINE>

    :param fileobj: the file-like object to write to
    :param catalog: the `Catalog` instance
    :param width: the maximum line width for the generated output; use `None`,
                  0, or a negative number to completely disable line wrapping
    :param no_location: do not emit a location comment for every message
    :param omit_header: do not include the ``msgid ""`` entry at the top of the
                        output
    :param sort_output: whether to sort the messages in the output by msgid
    :param sort_by_file: whether to sort the messages in the output by their
                         locations
    :param ignore_obsolete: whether to ignore obsolete messages and not include
                            them in the output; by default they are included as
                            comments
    :param include_previous: include the old msgid as a comment when
                             updating the catalog
    """
    def _normalize(key, prefix=''):
        return normalize(key, prefix=prefix, width=width) \
            .encode(catalog.charset, 'backslashreplace')

    def _write(text):
        if isinstance(text, unicode):
            text = text.encode(catalog.charset)
        fileobj.write(text)

    def _write_comment(comment, prefix=''):
        lines = comment
        if width and width > 0:
            lines = wrap(comment, width, break_long_words=False)
        for line in lines:
            _write('#%s %s\n' % (prefix, line.strip()))

    def _write_message(message, prefix=''):
        if isinstance(message.id, (list, tuple)):
            _write('%smsgid %s\n' % (prefix, _normalize(message.id[0], prefix)))
            _write('%smsgid_plural %s\n' % (
                prefix, _normalize(message.id[1], prefix)
            ))
            for i, string in enumerate(message.string):
                _write('%smsgstr[%d] %s\n' % (
                    prefix, i, _normalize(message.string[i], prefix)
                ))
        else:
            _write('%smsgid %s\n' % (prefix, _normalize(message.id, prefix)))
            _write('%smsgstr %s\n' % (
                prefix, _normalize(message.string or '', prefix)
            ))

    messages = list(catalog)
    if sort_output:
        messages.sort()
    elif sort_by_file:
        messages.sort(lambda x,y: cmp(x.locations, y.locations))

    for message in messages:
        if not message.id: # This is the header "message"
            if omit_header:
                continue
            comment_header = catalog.header_comment
            if width and width > 0:
                lines = []
                for line in comment_header.splitlines():
                    lines += wrap(line, width=width, subsequent_indent='# ',
                                  break_long_words=False)
                comment_header = u'\n'.join(lines) + u'\n'
            _write(comment_header)

        for comment in message.user_comments:
            _write_comment(comment)
        for comment in message.auto_comments:
            _write_comment(comment, prefix='.')

        if not no_location:
            for filename, lineno in message.locations:
                _write_comment(u'%s:%d' % (filename.replace(os.sep, '/'), 
                                           lineno), prefix=':')

        if message.flags:
            _write('#%s\n' % ', '.join([''] + list(message.flags)))

        if message.previous_id and include_previous:
            _write_comment(u'msgid %s' % _normalize(message.previous_id[0]),
                           prefix='|')
            if len(message.previous_id) > 1:
                _write_comment(u'msgid_plural %s' % _normalize(
                    message.previous_id[1]
                ), prefix='|')

        _write_message(message)
        _write('\n')

    if not ignore_obsolete:
        for message in catalog.obsolete.values():
            for comment in message.user_comments:
                _write_comment(comment)
            _write_message(message, prefix='#~ ')
            _write('\n')
