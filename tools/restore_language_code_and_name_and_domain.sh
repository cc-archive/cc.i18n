#!/bin/sh -x

# This is even more terrible, but it, too, works.

find ../cc/i18n/i18n | grep po$ | grep -v icommons \
 | xargs -l1 python restore_language_code_and_name_and_domain.py
