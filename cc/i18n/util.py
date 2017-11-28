"""
Utilities relevant to cc.i18n.
"""

import csv
import os
import pkg_resources

from cc.i18n.tools.transstats import CSV_HEADERS, DEFAULT_CSV_FILE


MO_PATH = pkg_resources.resource_filename(
    'cc.i18n', 'mo')

# Percent translated that languages should be at or above
TRANSLATION_THRESHOLD = 80


CACHED_TRANS_STATS = {}
def get_all_trans_stats(trans_file=DEFAULT_CSV_FILE):
    """
    Get all of the statistics on all translations, how much they are done

    Keyword arguments:
    - trans_file: specify from which CSV file we're gathering statistics.
        Used for testing, You probably don't need this.

    Returns:
      A dictionary of dictionaries formatted like:
      {'no': {  # key is the language name
         'num_messages': 564,  # number of messages, total
         'num_trans': 400,  # number of messages translated
         'num_fuzzy': 14,  # number of fuzzy messages
         'num_untrans': 150,  # number of untranslated, non-fuzzy messages
         'percent_trans': 70},  # percentage of file translated
       [...]}
    """
    # return cached statistics, if available
    if trans_file in CACHED_TRANS_STATS:
        return CACHED_TRANS_STATS[trans_file]

    if not os.path.exists(trans_file):
        raise IOError(
            "No such CSV file.  Maybe run ./bin/transstats in cc.i18n?")

    reader = csv.DictReader(file(trans_file, 'r'), CSV_HEADERS)
    stats = {}

    # record statistics
    for line in reader:
        num_messages = int(line['num_messages'])
        num_trans = int(line['num_trans'])
        num_fuzzy = int(line['num_fuzzy'])
        num_untrans = num_messages - num_trans - num_fuzzy
        percent_trans = int(line['percent_trans'])

        stats[line['lang']] = {
            'num_messages': num_messages,
            'num_trans': num_trans,
            'num_fuzzy': num_fuzzy,
            'num_untrans': num_untrans,
            'percent_trans': percent_trans}

    # cache and return
    CACHED_TRANS_STATS[trans_file] = stats
    return stats


CACHED_LANGUAGES_SUPPORTED = {}
def get_all_supported_languages(trans_file=DEFAULT_CSV_FILE):

    if trans_file in CACHED_LANGUAGES_SUPPORTED:
        return CACHED_LANGUAGES_SUPPORTED[trans_file]
    
    supported = set(get_all_trans_stats(trans_file).keys())
    CACHED_LANGUAGES_SUPPORTED[trans_file] = supported
    return supported


CACHED_WELL_TRANSLATED_LANGS = {}
def get_well_translated_langs(threshold=TRANSLATION_THRESHOLD,
                              trans_file=DEFAULT_CSV_FILE,
                              append_english=True):
    """
    Get an alphebatized and name-rendered list of all languages above
    a certain threshold of translation.
    
    Keyword arguments:
    - threshold: percentage that languages should be translated at or above
    - trans_file: specify from which CSV file we're gathering statistics.
        Used for testing, You probably don't need this.
    - append_english: Add English to the list, even if it's completely
        "untranslated" (since English is the default for messages,
        nobody translates it)

    Returns:
      An alphebatized sequence of dicts, where each element consists
      of the following keys:
       - code: the language code
       - name: the translated name of this language
      for each available language.
      An unsorted set of all qualified language codes
    """
    from cc.i18n import mappers

    cache_key = (threshold, trans_file, append_english)

    if cache_key in CACHED_WELL_TRANSLATED_LANGS:
        return CACHED_WELL_TRANSLATED_LANGS[cache_key]

    trans_stats = get_all_trans_stats(trans_file)
    
    qualified_langs = set([
        lang for lang, data in trans_stats.iteritems()
        if data['percent_trans'] >= threshold])

    # Add english if necessary.
    if not 'en' in qualified_langs and append_english:
        qualified_langs.add('en')

    # this loop is long hand for clarity; it's only done once, so
    # the additional performance cost should be negligible
    result = []

    for code in qualified_langs:
        from cc.i18n.gettext_i18n import ugettext_for_locale
        gettext = ugettext_for_locale(code)
        if code in mappers.LANG_MAP:
            # we have a translation for this name...
            name = gettext(mappers.LANG_MAP[code])
            result.append(dict(code=code, name=name))

    result = sorted(result, key=lambda lang: lang['name'].lower())
    
    CACHED_WELL_TRANSLATED_LANGS[cache_key] = result
    
    return result


# Locale negotiation tools
CACHED_APPLICABLE_LANGS = {}


def negotiate_locale(locale, mo_path=MO_PATH):
    """
    Choose the appropriate locale, using fallbacks, given the
    'requested' locale.

    Actually just a wrapper function for applicable_langs().
    """
    return applicable_langs(locale, mo_path)[0]


def applicable_langs(locale, mo_path=MO_PATH):
    """
    Return all available languages "applicable" to a requested locale.
    """
    cache_key = (locale, mo_path)
    if cache_key in CACHED_APPLICABLE_LANGS:
        return CACHED_APPLICABLE_LANGS[cache_key]

    applicable_langs = []
    if os.path.exists(os.path.join(mo_path, locale)):
        applicable_langs.append(locale)

    if '_' in locale:
        root_lang = locale.split('_')[0]
        if os.path.exists(os.path.join(mo_path, root_lang)):
            applicable_langs.append(root_lang)

    if not 'en' in applicable_langs:
        applicable_langs.append('en')

    # Don't cache silly languages that only fallback to en anyway, to
    # (semi-)prevent caching infinite amounts of BS
    if not locale == 'en' and len(applicable_langs) == 1:
        return applicable_langs
    
    CACHED_APPLICABLE_LANGS[cache_key] = applicable_langs
    return applicable_langs


def locale_to_lower_upper(locale):
    """
    Take a locale, regardless of style, and format it like "en-us"
    """
    if '-' in locale:
        lang, country = locale.split('-', 1)
        return '%s_%s' % (lang.lower(), country.upper())
    elif '_' in locale:
        lang, country = locale.split('_', 1)
        return '%s_%s' % (lang.lower(), country.upper())
    else:
        return locale.lower()


def locale_to_lower_lower(locale):
    """
    Take a locale, regardless of style, and format it like "en_US"
    """
    if '_' in locale:
        lang, country = locale.split('_', 1)
        return '%s-%s' % (lang.lower(), country.lower())
    else:
        return locale.lower()
