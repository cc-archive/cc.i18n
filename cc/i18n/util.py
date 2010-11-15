"""
Utilities relevant to cc.i18n.
"""

import csv
import os

from cc.i18n.tools.transstats import CSV_HEADERS, DEFAULT_CSV_FILE
from cc.i18n.gettext_i18n import ugettext_for_locale


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
    if CACHED_TRANS_STATS.has_key(trans_file):
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


CACHED_WELL_TRANSLATED_LANGS = {}
def get_well_translated_langs(threshold=TRANSLATION_THRESHOLD,
                              trans_file=DEFAULT_CSV_FILE):
    """
    Get a list of all languages above a certain threshold of translation.
    
    Keyword arguments:
    - threshold: percentage that languages should be translated at or above
    - trans_file:levelspecify from which CSV file we're gathering statistics.
        Used for testing, You probably don't need this.

    Returns:
      An unsorted set of all qualified language codes
    """
    if CACHED_WELL_TRANSLATED_LANGS.has_key((threshold, trans_file)):
        return CACHED_WELL_TRANSLATED_LANGS[(threshold, trans_file)]

    trans_stats = get_all_trans_stats(trans_file)
    
    qualified_langs = set([
        lang for lang, data in trans_stats.iter_items()
        if data['percent_trans'] >= threshold])

    CACHED_WELL_TRANSLATED_LANGS[(threshold, trans_file)] = qualified_langs
    
    return qualified_langs


# wow, this is really gross and long
CACHED_ALPHABETIZED_TRANSLATED_LANGS = {}
def alphabetized_well_translated_langs(threshold, trans_file):
    """
    Get an alphebatized and name-rendered list of all languages above
    a certain threshold of translation.

    Keyword arguments:
    - threshold: percentage that languages should be translated at or above
    - trans_file:levelspecify from which CSV file we're gathering statistics.
        Used for testing, You probably don't need this.

    Returns:
      An alphebatized sequence of dicts, where each element consists
      of the following keys:
       - code: the language code
       - name: the translated name of this language
      for each available language.
    """
    cache_key = (threshold, trans_file)
    if CACHED_ALPHABETIZED_TRANSLATED_LANGS.has_key(cache_key):
        return CACHED_ALPHABETIZED_TRANSLATED_LANGS[cache_key]
    
    translated_langs = get_well_translated_langs(threshold, trans_file)

    # this loop is long hand for clarity; it's only done once, so
    # the additional performance cost should be negligible
    result = []
    for code in translated_langs:
        gettext = ugettext_for_locale(code)
        name = gettext(u'lang.%s' % code)
        if name != u'lang.%s' % code:
            # we have a translation for this name...
            result.append(dict(code=code, name=name))

    result = sorted(result, key=lambda lang: lang['name'].lower())
    
    CACHED_ALPHABETIZED_TRANSLATED_LANGS[cache_key] = result

    return result
