from cc.i18n.tools import cc2po, po2cc

import polib

import os
import pkg_resources
import tempfile


FAKE_PO_DIR = pkg_resources.resource_filename(
    'cc.i18n.tests', 'fake_podir')
FAKE_I18N_DIR = pkg_resources.resource_filename(
    'cc.i18n.tests', 'fake_i18ndir')
FAKE_MASTER_PO = pkg_resources.resource_filename(
    'cc.i18n.tests', 'fake_master_ccorg.po')


def assert_catalogs_match(catalog1, catalog2):
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
        assert entry.msgstr == entry2.msgstr
        assert entry.msgctxt == entry2.msgctxt
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


def test_cc_to_po_tool():
    """
    Test the ./bin/cc2po tools' main method, see if it writes out
    files that match what we expect.
    """
    # Convert files, save to temp directory

    # Match "expected" output to actual output.
    pass
