## Copyright (c) 2010 Nathan R. Yergler, Christopher Webber, Creative Commons

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.

from setuptools import setup, find_packages

setup(
    name='cc.i18n',
    namespace_packages = ['cc',],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    version = "0.3",
    include_package_data = True,
    zip_safe = False,

    # scripts and dependencies
    install_requires = [
        'setuptools',
        'Babel>0.99',
        'zope.i18n',
        'python-gettext<2.0',
        'polib',
        'nose',
        'rdflib<3.0',
        'jinja2',
        ],

    entry_points = {
        'console_scripts': [
            'report = cc.i18n.tools.report:cli',
            'transstats = cc.i18n.tools.transstats:cli',
            'compile_mo = cc.i18n.tools.compile_mo:compile_mo_files',
            ],
        'zc.buildout': [
            'compile_mo = cc.i18n.tools.compile_mo:CompileMORecipe',
            'transstats = cc.i18n.tools.transstats:TransStatsRecipe',
            ],
        'babel.extractors': [
            'ccrdf = cc.i18n.tools.extractors:extract_translations_from_rdf',
            ],
        },

    # author metadata
    author = 'Nathan R. Yergler',
    author_email = 'nathan@creativecommons.org',
    description = '',
    license = 'MIT',
    url = 'http://translate.creativecommons.org',
    )
