import os
import gettext
import pkg_resources


MO_PATH = pkg_resources.resource_filename(
    'cc.i18npkg', 'mo')
I18N_DOMAIN = 'cc_org'
CCORG_GETTEXT_TRANSLATIONS = {}


def translations_for_locale(locale):
    if CCORG_GETTEXT_TRANSLATIONS.has_key(locale):
        return CCORG_GETTEXT_TRANSLATIONS[locale]

    # do I have the order backwards here?
    langs = [locale]
    if '_' in locale:
        root_lang = locale.split('_')[0]
        if os.path.exists(os.path.join(MO_PATH, root_lang)):
            langs.append(root_lang)

    langs.append('en')

    translations = gettext.translation(I18N_DOMAIN, MO_PATH, langs)
    CCORG_GETTEXT_TRANSLATIONS[locale] = translations
    return translations
