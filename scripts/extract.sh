#!/bin/bash

CWD=`pwd`
cd "$( dirname "${BASH_SOURCE[0]}" )/.."

pybabel extract -F babel.ini -o cc/i18n/po/en/cc_org.po .

cd "${CWD}"
