import polib

import copy

def defuzz(catalog):
    """Scan a catalog and de-fuzz-ify messages that have no translation."""

    for message in catalog:
        if 'fuzzy' in message.flags and (message.msgstr.strip() == u'' or 
                                         message.msgid.strip() == u''):
            # not fuzzy, damn it!
            message.flags.remove('fuzzy')

            
def reverse_english(message, english):
    """Look for the key of [message] (an instance of Message) as the string
    of a message in [english] (an instance of Catalog).  If found, return
    a new message whose key is the same as the English key.  If not found,
    return the original message."""

    result = copy.deepcopy(message)
    result.msgctxt = None # NOTE: Removing context from copied message
    # When we did not clear context, we got stray unrelated context 
    # stored in "result"
    # Context is irrelevant for these anyway, since they're PO-style

    hasYielded = False

    for en_msg in english:
        if en_msg.msgstr == message.msgid:
            # found it!
            result = copy.deepcopy(message)
            result.msgid = en_msg.msgid
            result.msgctxt = None

            hasYielded = True
            yield result

    if not hasYielded:
        yield result

def po_to_cc(source, english, fallback=True):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Message strings in [english]; if a 
    match is found, the key is replaced with the key from the [english] match.
    If more than one match is found, multiple strings are created.
    The result is a Catalog whose keys are symbolic rather than English text.

    Returns a Catalog instance."""

    # create the new target Catalog
    target = polib.POFile()

    # iterate over all the strings in the target PO
    for message in source:

        # skip messages w/an empty id
        if not(message.msgid): continue

        for new_message in reverse_english(message, english):
        
            # fall-back to English if untranslated
            if fallback and not(new_message.msgstr.strip()):
                new_message.msgstr = english.find(new_message.msgid).msgstr

            target.append(new_message)

    return target

def cc_to_po(source, english, previous=None):
    """Create a Catalog based on [source] (a Catalog instance).  Each Message
    key in [source] is checked against Messages in [english].  If a Message
    with the same ID is found in [english], the ID is replaced with the 
    English text.  The result is a Catalog whose keys contain English text
    rather than symbolic strings.

    Furthermore, each message in the new Catalog has as its .msgctxt
    the sybolic key value.

    Returns a Catalog instance."""

    # create the new target Catalog
    target = polib.POFile()

    # iterate over all the strings in the target PO
    for message in source:
        
        # make a copy of the original
        new_message = copy.deepcopy(message)

        english_message = english.find(message.msgid)
        if english_message:
            if english_message.msgstr:
                # only use the english text as a key if the text exists
                new_message.msgid = english_message.msgstr
        else:
            # if the key doesn't exist in the master file, 
            # it's dead to us.
            continue

        # if the string matches the key (ie, untranslated)
        #if new_message.msgid == new_message.msgstr:
        #    # clear the string
        #    new_message.msgstr = ''

        if previous is not None:

            # see if this was untranslated previously (in which case
            # we really just want to fall back to the new English instead
            # of the old)
            if previous.find(message.msgid):
                if new_message.msgstr == previous.find(message.msgid).msgstr:
                    # the string is the same as the old English text...
                    # remove the string since it's not really translated
                    pass
                    #new_message.msgstr = ''

            # see if this should be marked as "fuzzy"
            if new_message.msgstr and \
                    previous.find(message.msgid) \
                    and english.find(message.msgid):
                if previous.find(message.msgid).msgstr \
                        != english.find(message.msgid).msgstr:
                    new_message.flags.add('fuzzy')

        if new_message.msgid != message.msgid:
            new_message.msgctxt = message.msgid
        target.append(new_message)

    return target

