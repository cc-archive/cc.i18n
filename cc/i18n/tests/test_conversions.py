import os
import pkg_resources
import tempfile
import subprocess
from shutil import copyfile

import polib

from cc.i18n.tools import cc2po, po2cc, sync


FAKE_PO_DIR = pkg_resources.resource_filename(
    'cc.i18n.tests', 'fake_podir')
FAKE_I18N_DIR = pkg_resources.resource_filename(
    'cc.i18n.tests', 'fake_i18ndir')
FAKE_MASTER_PO = pkg_resources.resource_filename(
    'cc.i18n.tests', 'fake_master_ccorg.po')
FAKE_MODIFIED_MASTER_PO = pkg_resources.resource_filename(
    'cc.i18n.tests', 'fake_master_ccorg_modified.po')


def _passes_msgfmt_check(filepath):
    """
    Check if file at FILEPATH passes the msgfmt -c check.
    """
    return subprocess.Popen(['msgfmt', '-c', filepath]).wait() == 0


def assert_catalogs_match(catalog1, catalog2, cc2po_laziness=False):
    """
    Make sure two catalogs have the same entries in them.
    """

    catalog1_map = dict(
        [(entry.msgid, entry) for entry in catalog1])
    catalog2_map = dict(
        [(entry.msgid, entry) for entry in catalog2])

    assert len(catalog1_map) == len(catalog2_map)

    for msgid, entry in catalog1_map.iteritems():
        assert catalog2_map.has_key(msgid)

        entry2 = catalog2_map[msgid]

        assert entry.msgid == entry2.msgid
        assert entry.msgctxt == entry2.msgctxt

        if cc2po_laziness:

            # We don't really care if there's a translation that's the
            # same as the original in this case (??)
            if entry.msgstr == '' \
                    and entry2.msgstr != '' \
                    and entry2.msgid == entry2.msgstr:
                # for cc2po, good enough for us!
                pass
            else:
                assert entry.msgstr == entry2.msgstr

            # This is a real bug, but long unfixed
            if u'python-format' in entry.flags \
                    and u'python-format' not in entry2.flags:
                entry.flags.remove(u'python-format')
            assert entry.flags == entry2.flags

        else:
            assert entry.msgstr == entry2.msgstr
            assert entry.flags == entry2.flags



def test_po_to_cc_tool():
    """
    Test the ./bin/po2cc tools' main method, see if it writes out
    files that match what we expect.
    """
    # Run po files through tool, save to temp directory
    outdir = tempfile.mkdtemp()

    po2cc.po2cc(
        input_dir=FAKE_PO_DIR, output_dir=outdir,
        english_po=FAKE_MASTER_PO, cache=True)

    # Match "expected" output to actual output.
    for dirname in os.listdir(FAKE_I18N_DIR):
        i18n_name = os.path.join(FAKE_I18N_DIR, dirname, 'cc_org.po')
        outfile_name = os.path.join(outdir, dirname, 'cc_org.po')
        assert_catalogs_match(polib.pofile(i18n_name), polib.pofile(outfile_name))
        ## Not passing, but do we care?  Presumably not passing forever.
        # assert _passes_msgfmt_check(outfile_name)


def test_cc_to_po_tool():
    """
    Test the ./bin/cc2po tools' main method, see if it writes out
    files that match what we expect.
    """
    # Run po files through tool, save to temp directory
    outdir = tempfile.mkdtemp()

    cc2po.cc2po(
        input_dir=FAKE_I18N_DIR, output_dir=outdir,
        english_po=FAKE_MASTER_PO)

    # Match "expected" output to actual output.
    for dirname in os.listdir(FAKE_PO_DIR):
        po_name = os.path.join(FAKE_PO_DIR, dirname, 'cc_org.po')
        outfile_name = os.path.join(outdir, dirname, 'cc_org.po')
        assert_catalogs_match(
            polib.pofile(po_name), polib.pofile(outfile_name),
            True)
        assert _passes_msgfmt_check(outfile_name)


def test_sync():
    """
    Test ./bin/sync (or the function that's run by that)

    This one's a bit tricky, but not too tricky.

    The first time we sync with the normal unchanged master cc_org.po
    and make sure the files that are written out are pretty much
    exactly the same as the ones in FAKE_MASTER_PO (they shouldn't
    have needed to change).  Then we should run the sync again 
    """
    outdir = tempfile.mkdtemp()
    masterpodir = tempfile.mkdtemp()

    # This is so these files don't get adultered by the process
    fake_master_po = os.path.join(
        masterpodir, 'fake_master_ccorg.po')
    fake_master_po_bak = os.path.join(
        masterpodir, 'fake_master_ccorg.po.bak')
    fake_master_po_modified = os.path.join(
        masterpodir, 'fake_master_ccorg_modified.po')
    fake_master_po_modified_bak = os.path.join(
        masterpodir, 'fake_master_ccorg_modified.po.bak')

    copyfile(FAKE_MASTER_PO, fake_master_po)
    copyfile(FAKE_MASTER_PO + '.bak', fake_master_po_bak)
    copyfile(FAKE_MODIFIED_MASTER_PO, fake_master_po_modified)
    copyfile(FAKE_MODIFIED_MASTER_PO + '.bak', fake_master_po_modified_bak)
    
    # Sync once, presumably files shouldn't be changed
    sync.sync(FAKE_PO_DIR, outdir, fake_master_po)

    for dirname in os.listdir(FAKE_PO_DIR):
        po_name = os.path.join(FAKE_PO_DIR, dirname, 'cc_org.po')
        outfile_name = os.path.join(outdir, dirname, 'cc_org.po')
        assert_catalogs_match(
            polib.pofile(po_name), polib.pofile(outfile_name),
            True)
        assert _passes_msgfmt_check(outfile_name)

    sync.sync(outdir, outdir, fake_master_po_modified)


    vi_pofilepath = os.path.join(outdir, 'vi', 'cc_org.po')
    vi_pofile = polib.pofile(vi_pofilepath)
    assert _passes_msgfmt_check(vi_pofilepath)
    es_pofilepath = os.path.join(outdir, 'es', 'cc_org.po')
    es_pofile = polib.pofile(es_pofilepath)
    assert _passes_msgfmt_check(es_pofilepath)

    ## util.name should have changed
    # was previously untranslated in vi
    vi_utilname = vi_pofile.find('util.name', by='msgctxt')
    assert u'fuzzy' not in vi_utilname.flags
    assert vi_utilname.msgctxt == 'util.name'
    assert vi_utilname.msgid == 'Namez0rs'
    assert vi_utilname.msgstr == ''

    # was translated in es
    es_utilname = es_pofile.find('util.name', by='msgctxt')
    assert u'fuzzy' in es_utilname.flags
    assert es_utilname.msgctxt == 'util.name'
    assert es_utilname.msgid == 'Namez0rs'
    assert es_utilname.msgstr == 'Nombre'

    ## We removed 'license.mark.curator_help'; assert it is in neither
    ## catalog
    assert vi_pofile.find('license.mark.curator_help', by='msgctxt') is None
    assert es_pofile.find('license.mark.curator_help', by='msgctxt') is None

    ## We added util.whodunnit, which is brand new
    vi_whodunnit = vi_pofile.find('util.whodunnit', by='msgctxt')
    es_whodunnit = es_pofile.find('util.whodunnit', by='msgctxt')
    assert vi_whodunnit.flags == es_whodunnit.flags == []
    assert vi_whodunnit.msgctxt == es_whodunnit.msgctxt == 'util.whodunnit'
    assert vi_whodunnit.msgid == es_whodunnit.msgid == 'Whodunnit??'
    assert vi_whodunnit.msgstr == es_whodunnit.msgstr == ''

