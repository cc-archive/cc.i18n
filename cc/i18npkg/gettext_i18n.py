import gettext
import pkg_resources

MO_PATH = pkg_resources.resource_filename(
    'cc.i18npkg', 'mo')
I18N_DOMAIN = 'cc_org'
CCORG_GETTEXT = gettext.translation(I18N_DOMAIN, MO_PATH)
