import optparse

def make_option_parser():
    """Return an optparse.OptionParser configured for the make_cc_files 
    command line script."""

    parser = optparse.OptionParser()

    # settings
    parser.add_option('-e', '--english', dest='english_po',
                      default='i18n/en/cc_org.po',
                      help='English .po file, used to map keys.')

    # input options
    parser.add_option('-i', '--input-dir', dest='input_dir',
                      help='Directory to search for .po files to convert.')

    # output options
    parser.add_option('-o', '--output-dir', dest='output_dir', 
                      help='Output directory for CC-style .po files.')

    return parser
