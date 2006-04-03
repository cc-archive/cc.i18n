#!/usr/bin/env python

# istr2po.py [directory ...]
# dumps corresponding .po files in current dir

import sys
import os
import re

def loadFiles(dirPath):
    """Read all .html files from the specified [dirPath] and return a
    dictionary mapping file names (sans .html) to contents."""

    # initialize the string buffer
    buffer = {}
    
    files = os.listdir(dirPath)
    files.sort()

    for fname in files:
        if (fname[-5:] != '.html'):
            continue

        f = file(os.path.join(dirPath, fname))
        s = f.read()
        s = re.sub(r'"',r'\\"',s) # escapes " character
        s = re.sub(r'\r\n',r'\n',s) # removes line feeds
        s = re.sub(r'\s+$',r'',s) # removes space at the end of the line
        s = re.sub(r'^\s+',r'',s) # removes spaces at the beginning of the line
        s = re.sub(r'\n',r'\\n',s) # escapes CR
        s = re.sub(r'@(\S+?)@',r'${\1}',s) # converts @ fields @
        msgid = fname[:-5]

        buffer[msgid] = s

    return buffer

if __name__ == '__main__':

    # if CVS gets included, remove it
    if 'CVS' in sys.argv:
        sys.argv.remove('CVS')

    # for each directory specified on the command line...
    dirnames = [n for n in sys.argv if n != 'CVS' and os.path.isdir(n) ]
    
    for dir in dirnames:

        # check if this is a country specific locale (i.e., en_US)
        if len(os.path.basename(dir).split('_')) > 1 and \
           os.path.exists( os.path.join(
                os.path.dirname(dir),
                os.path.basename(dir).split('_')[0])
            ):

            parent_locale_dir = os.path.join(
                os.path.dirname(dir),
                os.path.basename(dir).split('_')[0])

            # first load the base locale
            i18n_strings = loadFiles(parent_locale_dir)
        else:
            i18n_strings = {}
            
        # load the strings
        i18n_strings.update(loadFiles(dir))

        # write out the .po file
        buf = ''
        buf += 'msgid ""\n'
        buf += 'msgstr ""\n'
        buf += '"Content-Type: text/plain; charset=UTF-8\\n"\n'
        buf += '"Language-code: '+dir+'\\n"\n'
        buf += '"Language-name: '+dir+'\\n"\n'
        buf += '"Domain: icommons\\n"\n'
        
        for msgid in i18n_strings:
            buf += 'msgid "'+msgid+'"\n'
            buf += 'msgstr "'+i18n_strings[msgid]+'"\n'
            buf += '\n'
            
        pofile = file('icommons-'+dir+'.po','w+')
        pofile.write(buf)

