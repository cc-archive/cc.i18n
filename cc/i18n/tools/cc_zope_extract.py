"""
Extract Zope translation stuff

Extract both 
"""

import optparse

from zope.app.locales.extract import POTMaker, POTEntry
from zope.app.locales.extract import py_strings
from zope.app.locales.extract import tal_strings
from babel.messages.pofile import normalize
from zope.i18nmessageid import Message

from zope.app.locales.pygettext import make_escapes
make_escapes(1)

class CCPOTEntry(POTEntry):
    def write(self, file):
        if (isinstance(self.msgid, Message) and
            self.msgid.default is not None):

            # Write Default
            default = self.msgid.default.strip()
            lines = normalize(default).split("\n")
            lines[0] = "#. Default: %s\n" % lines[0]
            for i in range(1, len(lines)):
                lines[i] = "#. %s\n" % lines[i]
            file.write("".join(lines))

        if self.comments:
            file.write(self.comments)
        file.write('msgid %s\n' % normalize(self.msgid))

        if (isinstance(self.msgid, Message) and
            self.msgid.default is not None):
            # Write msgstr
            file.write('msgstr %s\n' % normalize(default))
        else:
            file.write('msgstr ""\n')

        file.write('\n')


class CCPOTMaker(POTMaker):
    def add(self, strings, base_dir=None):
        for msgid, locations in strings.items():
            if msgid == '':
                continue
            if msgid not in self.catalog:
                self.catalog[msgid] = CCPOTEntry(msgid)

            for filename, lineno in locations:
                if base_dir is not None:
                    filename = filename.replace(base_dir, '')
                self.catalog[msgid].addLocationComment(filename, lineno)


def extract_stuff(outfile, py_dirs, zpt_dirs, domain="cc_org"):
    maker = CCPOTMaker(outfile, '')

    for py_dir in py_dirs:
        maker.add(
            py_strings(py_dir, 'cc_org'),
            py_dir)

    for zpt_dir in zpt_dirs:
        maker.add(
            tal_strings(zpt_dir, 'cc_org', include_default_domain=True),
            zpt_dir)

    maker.write()

def main():
    parser = optparse.OptionParser()

    parser.add_option(
        '-p', '--py-paths', dest="py_paths",
        help=(
            "Base python module to import from, comma separated.\n"
            "EG: 'cc.engine,cc.license'"))
    parser.add_option(
        '-z', '--zpt-paths', dest="zpt_paths",
        help=(
            "module:paths to import ZPT files from, comma separated.\n"
            "EG: 'cc.engine:templates,cc.zillywoo:templates'"))

    parser.add_option(
        '-d', '--domain', dest="domain",
        help=(
            "Translation domain we're extracting for"))

    
    options, args = parser.parse_args()

    if not (options.py_paths or options.zpt_paths):
        parser.error("One of python paths or zpt paths must be provided")

    
