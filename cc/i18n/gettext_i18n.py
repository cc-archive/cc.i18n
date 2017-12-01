import os
import gettext
import pkg_resources

import six

from cc.i18n.util import applicable_langs, MO_PATH


I18N_DOMAIN = 'cc_org'
CCORG_GETTEXT_TRANSLATIONS = {}


def translations_for_locale(locale, mo_path=MO_PATH):
    """
    Get the right translation and return it
    """
    cache_key = (locale, mo_path)
    if cache_key in CCORG_GETTEXT_TRANSLATIONS:
        return CCORG_GETTEXT_TRANSLATIONS[cache_key]

    # do I have the order backwards here?
    langs = applicable_langs(locale, mo_path)

    translations = None

    for lang in langs:
        full_mo_path = os.path.join(mo_path, lang, 'LC_MESSAGES', 'cc_org.mo')
        if not os.path.exists(full_mo_path):
            continue

        this_trans = gettext.GNUTranslations(open(full_mo_path, 'rb'))

        if translations is None:
            translations = this_trans
        else:
            translations.add_fallback(this_trans)

    CCORG_GETTEXT_TRANSLATIONS[cache_key] = translations
    return translations


def ugettext_for_locale(locale, mo_path=MO_PATH):
    def _wrapped_ugettext(message):
        message = translations_for_locale(
            locale, mo_path).gettext(message)
        # Use gettext so it works on Python 2 and 3 (which doesn't have
        #   ugettext).
        # Use the old Python 2 double-check code to ensure unicode.
        if isinstance(message, six.text_type):
            return message
        else:
            return message.decode(u'utf-8')

    return _wrapped_ugettext


def fake_ugettext(string):
    """
    Fake that we're making a gettext call for extraction purposes.
    """
    return string
