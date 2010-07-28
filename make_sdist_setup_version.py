# This hacky hacky script should be able to make a new setup.py file
# and run sdist on it to create a tarball with a date-based version
# number.

import datetime
import os
import re

# A big ol' version number based off of present time
this_dir = os.path.dirname(os.path.abspath(__file__))

now_version = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

setup_data = file(os.path.join(this_dir, 'setup.py')).read()
new_setup_data = re.sub(
    "version ?= ?[\"'][a-zA-Z0-9_.]*[\"']",
    'version = "%s"'% now_version,
    setup_data)

file(os.path.join(this_dir, 'tmp_sdist_setup.py'), 'w').write(
    new_setup_data)
