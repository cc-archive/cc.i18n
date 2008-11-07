import os
import optparse
import copy
import logging
from logging import getLogger

from babel.messages.pofile import read_po
from babel.messages.catalog import Catalog, Message

from babel.messages.pofile import write_po

def defuzz(catalog):
    """Scan a catalog and de-fuzz-ify messages that have no translation."""

    for message in catalog:
        if message.fuzzy and (message.string.strip() == u'' or 
                              message.id.strip() == u''):
            # not fuzzy, damn it!
            message.flags.remove('fuzzy')

            
def reverse_english(message, english):
    """Look for the key of [message] (an instance of Message) as the string
    of a message in [english] (an instance of Catalog).  If found, return
    a new message whose key is the same as the English key.  If not found,
    return the original message."""

    result = copy.deepcopy(message)
    hasYielded = False

    for en_msg in english:
        if en_msg.string == message.id:
            # found it!
            result = copy.deepcopy(message)
            result.id = en_msg.id

            hasYielded = True
            yield result

    if not hasYielded:
        yield result

def po_to_cc(source, english):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Message strings in [english]; if a 
    match is found, the key is replaced with the key from the [english] match.
    If more than one match is found, multiple strings are created.
    The result is a Catalog whose keys are symbolic rather than English text.

    Returns a Catalog instance."""

    # create the new target Catalog
    target = Catalog(header_comment="", 
                     locale=source.locale, 
                     domain=source.domain)

    # iterate over all the strings in the target PO
    for message in source:

        # skip messages w/an empty id
        if not(message.id): continue

        for new_message in reverse_english(message, english):
        
            # fall-back to English if untranslated
            if not(new_message.string.strip()):
                new_message.string = english[new_message.id].string

            target[new_message.id] = new_message

    return target

def cc_to_po(source, english, previous=None):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Messages in [english].  If a Message
    with the same ID is found in [english], the ID is replaced with the 
    English text.  The result is a Catalog whose keys contain English text
    rather than symbolic strings.

    Furthermore, each message in the new Catalog has as its .context
    the sybolic key value.

    Returns a Catalog instance."""

    # create the new target Catalog
    target = Catalog()

    # iterate over all the strings in the target PO
    for message in source:
        
        # make a copy of the original
        new_message = copy.deepcopy(message)

        if message.id in english and english[message.id].string:
            # only use the english text as a key if the text exists
            new_message.id = english[message.id].string

        # if the string matches the key (ie, untranslated)
        #if new_message.id == new_message.string:
        #    # clear the string
        #    new_message.string = ''

        if previous is not None:

            # see if this was untranslated previously (in which case
            # we really just want to fall back to the new English instead
            # of the old)
            if message.id in previous:
                if new_message.string == previous[message.id].string:
                    # the string is the same as the old English text...
                    # remove the string since it's not really translated
                    pass
                    #new_message.string = ''

            # see if this should be marked as "fuzzy"
            if new_message.string and \
                    message.id in previous and message.id in english:
                if previous[message.id].string != english[message.id].string:
                    new_message.flags.add('fuzzy')

        if new_message.id != message.id:
            new_message.context = message.id
        target[new_message.id] = new_message

    return target

