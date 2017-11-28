"""
Compile .po files into .mo files in the cc
"""
from builtins import object

import os
import pkg_resources
from stat import ST_MTIME
import polib


I18N_PATH = pkg_resources.resource_filename(
    'cc.i18n', 'po')
MO_FILES_BASE = pkg_resources.resource_filename(
    'cc.i18n', 'mo')


def compile_mo_files(input_dir=I18N_PATH, output_dir=MO_FILES_BASE):
    """
    Compile all cc-style po files to mo files.

    Keyword arguments:
    - input_dir: Directory of input files to compile
    - output_dir: Directory where we'll put compiled MO files
    """
    for catalog in os.listdir(input_dir):
        catalog_path = os.path.join(input_dir, catalog)

        po_path = os.path.join(catalog_path, 'cc_org.po')

        if not os.path.isdir(catalog_path) or not os.path.exists(po_path):
            continue

        po_mtime = os.stat(po_path)[ST_MTIME]

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if not os.path.exists(os.path.join(output_dir, catalog)):
            os.mkdir(os.path.join(output_dir, catalog))
        if not os.path.exists(os.path.join(
                output_dir, catalog, 'LC_MESSAGES')):
            os.mkdir(os.path.join(
                    output_dir, catalog, 'LC_MESSAGES'))

        mo_path = os.path.join(
            output_dir, catalog, 'LC_MESSAGES', 'cc_org.mo')

        # don't compile mo files when we don't need to.
        if os.path.exists(mo_path):
            mo_mtime = os.stat(mo_path)[ST_MTIME]
            if po_mtime == mo_mtime:
                continue

        po = polib.pofile(po_path)
        po.save_as_mofile(mo_path)


class CompileMORecipe(object):
    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        options['path'] = MO_FILES_BASE

    def install(self):
        compile_mo_files()
        return ()

    update = install


if __name__ == '__main__':
    compile_mo_files()
