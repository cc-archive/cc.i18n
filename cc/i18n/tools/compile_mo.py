"""
Compile .po files into .mo files in the cc 
"""

import os
import pkg_resources
from pythongettext.msgfmt import Msgfmt


I18N_PATH = pkg_resources.resource_filename(
    'cc.i18n', 'i18n')
MO_FILES_BASE = pkg_resources.resource_filename(
    'cc.i18n', 'mo')


def compile_mo_files():
    for catalog in os.listdir(I18N_PATH):
        catalog_path = os.path.join(I18N_PATH, catalog)

        po_path = os.path.join(catalog_path, 'cc_org.po')

        if not os.path.isdir(catalog_path) or not os.path.exists(po_path):
            continue

        if not os.path.exists(MO_FILES_BASE):
            os.mkdir(MO_FILES_BASE)
        if not os.path.exists(os.path.join(MO_FILES_BASE, catalog)):
            os.mkdir(os.path.join(MO_FILES_BASE, catalog))
        if not os.path.exists(os.path.join(
                MO_FILES_BASE, catalog, 'LC_MESSAGES')):
            os.mkdir(os.path.join(
                    MO_FILES_BASE, catalog, 'LC_MESSAGES'))

        mo_path = os.path.join(
            MO_FILES_BASE, catalog, 'LC_MESSAGES', 'cc_org.mo')

        # TODO: only do this if po_mtime > mo_mtime maybe, see
        # zope.i18n.compile
        mo_data = Msgfmt(po_path, 'cc_org').getAsFile()
        fd = open(mo_path, 'wb')
        fd.write(mo_data.read())
        fd.close()


if __name__ == '__main__':
    compile_mo_files()
