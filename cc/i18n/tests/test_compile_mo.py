import pkg_resources
import tempfile

from cc.i18n.tools.compile_mo import compile_mo_files
from cc.i18n.gettext_i18n import ugettext_for_locale


def test_compile_mo_files():
    """
    Test that compile_mo_files compiles translations which actually
    have the appropriate output
    """
    output_dir = tempfile.mkdtemp()
    fake_i18ndir = pkg_resources.resource_filename(
        'cc.i18n.tests', 'fake_i18ndir')

    compile_mo_files(fake_i18ndir, output_dir)

    expected_translations = {
        'en': {
            'country.nz': 'New Zeland',
            'licenses.pretty_sampling': 'Sampling',
            'license.rdfa_licensed':
                ('${work_title} by ${work_author} is licensed under a '
                 '<a rel="license" href="${license_url}">Creative Commons '
                 '${license_name} License</a>')},
        'pt': {
            'country.nz': 'Nova Zel\xc3\xa2ndia',
            'licenses.pretty_sampling': 'Sampling',
            'license.rdfa_licensed':
                ('A obra ${work_title} de ${work_author} '
                 'foi licenciada com uma Licen\xc3\xa7a '
                 '<a rel="license" href="${license_url}>Creative Commons - '
                 '${license_name}</a>')},
        'es': {
            'country.nz': 'Nueva Zelanda',
            'licenses.pretty_sampling': 'Sampling',
            'license.rdfa_licensed':
                ('${work_title} por ${work_author} '
                 'se encuentra bajo una Licencia '
                 '<a rel="license" href="${license_url}">Creative Commons '
                 '${license_name}</a>')}}

    for language, expected_translations in expected_translations.iteritems():
        gettext = ugettext_for_locale(language, output_dir)
        for msgid, expected_translation in expected_translations.iteritems():
            assert gettext(msgid) == expected_translation

