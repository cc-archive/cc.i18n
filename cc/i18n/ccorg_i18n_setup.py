import pkg_resources
import os

from zope.i18n.translationdomain import TranslationDomain
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.compile import compile_mo_file

from zope import component


DOMAIN_SETUP = False

MO_PATH = pkg_resources.resource_filename(
    'cc.i18npkg', 'mo')
I18N_DOMAIN = 'cc_org'
# cc/i18npkg/mo/ms/LC_MESSAGES/cc_org.mo

def _setup_i18n():
    global DOMAIN_SETUP
    if DOMAIN_SETUP:
        return

    domain = TranslationDomain(I18N_DOMAIN)
    for catalog in os.listdir(MO_PATH):
        catalog_path = os.path.join(MO_PATH, catalog)

        mo_path = os.path.join(catalog_path, 'LC_MESSAGES', I18N_DOMAIN + '.mo')
        if not os.path.exists(mo_path):
            continue

        domain.addCatalog(UTF8GettextMessageCatalog(
                catalog, I18N_DOMAIN, mo_path))

    component.provideUtility(domain, ITranslationDomain, name='cc_org')
    DOMAIN_SETUP = True


class UTF8GettextMessageCatalog(GettextMessageCatalog):
    def queryMessage(self, id, default=None):
        try:
            return self._catalog.ugettext(id).decode('utf-8')
        except KeyError:
            return default


_setup_i18n()
