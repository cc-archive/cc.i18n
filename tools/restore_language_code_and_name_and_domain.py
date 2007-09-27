#!/usr/bin/python

import sys
import os

## This code is laugable and terrible.
## It also works.

extra = '"Language-code: %s\\n"\n"Language-name: %s\\n"\n"Domain: cc_org\\n"\n'
before = '"Generated-By: Babel 0.9.1\\n"\n'

if len(sys.argv) < 2:
	print "USAGE:\n"
	print "progname.py file_to_covert.po"
	sys.exit(1)

def find_language_code(filename):
	# hang on tight
	big = filename.split(os.path.sep)
	assert 'po' in big[-1]
	return big[-2]

filename = sys.argv[1]
file_contents = open(filename).read()

# If they don't want to be converted, so be it.
if before not in file_contents:
	print 'skipping', filename
	sys.exit(0)

# We better not dual-process things
assert 'Language-code: ' not in file_contents

first, rest = open(filename).read().split(before, 1)

lang_code = find_language_code(filename)
real_extra = extra % (lang_code, lang_code)
first += before + real_extra

outfd = open(filename, 'w')
outfd.write(first)
outfd.write(rest)
outfd.close()
