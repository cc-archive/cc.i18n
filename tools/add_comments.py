import babel.messages.pofile
import glob

def add_comments(english_po_filename, locale, non_english_po_filename):
    english_po = babel.messages.pofile.read_po(open(english_po_filename),
                                               domain = 'cc_org',
                                               locale = locale)
    target_po = babel.messages.pofile.read_po(open(non_english_po_filename))
    
    for message_name in target_po._messages:
        message_obj = target_po[message_name]
        if message_name not in english_po._messages:
            message_name = message_name.strip()
        try:
            english_value = english_po._messages[message_name].string
            message_obj.auto_comments = english_value.split('\n')
            message_obj.user_comments = []
        except:
            pass
            # print 'this is dumb, the key', message_name, 'is not available in English'
        
    print 'converted file', non_english_po_filename
    babel.messages.pofile.write_po(open(non_english_po_filename, 'w'), target_po)

def add_comments_to_all():
    english_filename = 'i18n/en/cc_org.po'
    for pofile in glob.glob('i18n/*/cc_org.po'):
        
        if pofile == english_filename:
            continue # Get me a non-English one
        
        print 'converting ', pofile
        add_comments(english_filename, pofile.split('/')[1], pofile )
    

if __name__ == '__main__':
    add_comments_to_all()
