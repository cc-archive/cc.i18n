import os
import optparse
import copy
import logging
from logging import getLogger

from babel.messages.pofile import read_po, write_po
from babel.messages.catalog import Catalog, Message

def reverse_english(message, english):
    """Look for the key of [message] (an instance of Message) as the string
    of a message in [english] (an instance of Catalog).  If found, return
    a new message whose key is the same as the English key.  If not found,
    return the original message."""

    for en_msg in english:
        if en_msg.string == message.id:
            # found it!
            result = copy.deepcopy(message)
            result.id = en_msg.id
            return result

    return copy.deepcopy(message)

def po_to_cc(source, english):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Message strings in [english]; if a 
    match is found, the key is replaced with the key from the [english] match.
    The result is a Catalog whose keys are symbolic rather than English text.

    Returns a Catalog instance."""

    # create the new target Catalog
    target = Catalog()

    # iterate over all the strings in the target PO
    for message in source:
        new_message = reverse_english(message, english)
        
        # fall-back to English if untranslated
        if not(new_message.string.strip()):
            new_message.string = english[new_message.id].string

        target[new_message.id] = new_message

    return target

def cc_to_po(source, english):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Messages in [english].  If a Message
    with the same ID is found in [english], the ID is replaced with the 
    English text.  The result is a Catalog whose keys contain English text
    rather than symbolic strings.

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
        if new_message.id == new_message.string:
            # clear the string
            new_message.string = ''

        target[new_message.id] = new_message

    return target

