#!/bin/bash

./istr2po.py *
cp *.po ../i18n/
rm -rf ../i18n/locales
mv locales ../i18n
